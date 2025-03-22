import os
from pathlib import Path
from dotenv import load_dotenv
import logging
from tqdm import tqdm

import asyncio
import requests

import cv2
import numpy as np

from cv_detection import CVDetector

load_dotenv()

# Configure logging format
logging.basicConfig(
    format="[%(asctime)s] %(message)s",  # Use %(asctime)s instead of %H:%M:%S
    datefmt="%H:%M:%S",  # Correct time formatting
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load API endpoints
BACKEND_API = os.environ.get('BACKEND_API')
if not BACKEND_API:
    raise ValueError("Error: BACKEND_API is not set in the environment variables.")

# Load different detectors
cv_detector = CVDetector(
    detection_model_checkpoint=os.environ.get('VEHICLE_DETECTION_CKPT'),
    classification_model_checkpoint=os.environ.get('ACCIDENT_CLASSIFICATION_CKPT'),
    logger=logger
)

"""
Sending data to backend
"""

async def send_traffic_data(results):
    """Sends processed traffic flow data to the backend."""
    logger.info('Sending data to backend api...')
    data = {
        "vehicle_count": results,
        "avg_speed": results,
        "traffic_density": results
    }

    # response = requests.post(BACKEND_API + '/traffic_update', json=data)
    # if response.status_code == 200:
    #     logger.info('Traffic data updated successfully.\n')
    # else:
        # logger.info('Failed to send traffic data.\n')

"""
Retrieve data for processing
"""

async def get_live_videos(prev_timestamp):
    """Retrieves live Singapore highway camera feed using LTA website"""
    LTA_API = "https://api.data.gov.sg/v1/transport/traffic-images"

    try:
        response = requests.get(LTA_API)
        response.raise_for_status()  # Raise an error for 4xx/5xx responses
        response = response.json()

    
        acquisition_timestamp, cameras = response['items'][0]['timestamp'], response['items'][0]['cameras']
        if acquisition_timestamp != prev_timestamp:
            logger.info('New data acquired from LTA API!')
            data = {}

            for camera in tqdm(cameras, desc='Processing new data...'):
                response = requests.get(camera['image'])
                img_array = np.frombuffer(response.content, np.uint8)
                image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

                data[camera['camera_id']] = {
                    'timestamp': camera['timestamp'],
                    'image_link': camera['image'],
                    'image': image,
                    'location': camera['location'],
                    'metadata': {
                        'image_height':camera['image_metadata']['height'],
                        'image_width':camera['image_metadata']['width']
                    }
                }

            return acquisition_timestamp, data
        return prev_timestamp, None

    except requests.exceptions.RequestException as e:
        logger.info(f'Error fetching data from LTA API: {e}')
        return prev_timestamp, None

def get_simulated_images():
    """Retrieves simulation data from a test image folder"""
    folder = r"../data/DETRAC_Upload"
    data = {}
    for idx, image in enumerate(sorted(Path(folder).rglob('*.jpg'))):
        data[idx] = {'image': image}
    return data

"""
Run asynchronous processing
"""

async def process_images(images):
    """Processes images for both congestion detection and optical flow asynchronously."""
    tasks = [
        asyncio.create_task(cv_detector.run_processing(images))
    ]
    await asyncio.gather(*tasks)

async def watcher(interval=60, wait=20):
    """Monitors for new images and triggers processing functions"""
    prev_timestamp = None
    frame_buffer = {}
    count = 0

    while True:
        count += 1

        # Fetch live images from lta
        prev_timestamp, images = await get_live_videos(prev_timestamp)
        # Fetch simulated images from folder
        # images = get_simulated_images()

        # Combines batches of data into singular dict
        if images:
            for camera_id, image_data in images.items():
                frame_buffer[camera_id] = frame_buffer.get(camera_id, []) + [image_data]
        
        # If interval period is up
        if count > interval // wait:
            logger.info('Processing data...')

            # Post processing
            results = await process_images(frame_buffer)
            await send_traffic_data(results)

            # Reset variables
            count = 0
            frame_buffer = {}

        await asyncio.sleep(wait)


if __name__=='__main__':
    logger.info('Starting watcher...')
    asyncio.run(watcher(interval=10, wait=5))
