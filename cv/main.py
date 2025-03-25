import os
import json
import logging
from tqdm import tqdm
from pathlib import Path
from dotenv import load_dotenv

import asyncio
import requests
import websockets

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

# Load endpoints
LTA_API = "https://api.data.gov.sg/v1/transport/traffic-images"
BACKEND_API = os.environ.get('BACKEND_API')
BACKEND_WS_API = os.environ.get('BACKEND_WS_API')


# Load different detectors
cv_detector = CVDetector(
    detection_model_checkpoint=os.environ.get('VEHICLE_DETECTION_CKPT'),
    classification_model_checkpoint=os.environ.get('ACCIDENT_CLASSIFICATION_CKPT'),
    logger=logger
)

"""
Sending data to backend
"""

async def send_traffic_data(images, frames, results):
    """Sends processed traffic flow data to the backend."""
    logger.info('Sending data to backend api...')
    data = {
        'cameras': images,
        'frames': frames,
        'results': results,
    }
    try:
        requests.post(BACKEND_API + '/traffic_update', json=data)
        logger.info("Traffic data sent successfully.\n")
    except Exception as e:
        logger.error(f"Failed to send traffic data: {e}\n")

"""
Retrieve data for processing
"""

async def get_live_videos(prev_timestamp):
    """Retrieves live Singapore highway camera feed using LTA website"""
    try:
        response = requests.get(LTA_API)
        response.raise_for_status()  # Raise an error for 4xx/5xx responses
        response = response.json()

    
        acquisition_timestamp, cameras = response['items'][0]['timestamp'], response['items'][0]['cameras']
        image_timestamp = cameras[0]['timestamp']

        if acquisition_timestamp != prev_timestamp:  # TODO: Switch to image_timestamp instead
            logger.info('New data acquired from LTA API!')
            data = {}

            for camera in tqdm(cameras, desc='Processing new data...'):
                response = requests.get(camera['image'])
                img_array = np.frombuffer(response.content, np.uint8)
                image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

                data[int(camera['camera_id'])] = {
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
    """Processes images for congestion detection, optical flow and accident classification asynchronously."""
    try:
        return await cv_detector.run_processing(images)
    except Exception as e:
        logger.error(f"Error processing images: {e}")
        return {}
    
async def retrieve_camera_data(frames):
    """Extracts camera metadata from live data"""
    return {
        int(camera_id): {
            'lat': data_items[0]['location']['latitude'],
            'long': data_items[0]['location']['longitude'],
            'description': 'test'
        } for camera_id, data_items in frames.items()
    }

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

        # Combines batches of data into singular dict for time-series data
        if images:
            for camera_id, image_data in images.items():
                frame_buffer[int(camera_id)] = frame_buffer.get(int(camera_id), []) + [image_data]
        
        # If interval period is up
        if count > interval // wait:
            logger.info('Processing data...')

            # Post processing
            camera_data = await retrieve_camera_data(frame_buffer)
            frame_buffer, results = await process_images(frame_buffer)
            await send_traffic_data(camera_data, frame_buffer.copy(), results)

            # Reset variables
            count = 0
            frame_buffer = {}

        await asyncio.sleep(wait)


if __name__=='__main__':
    logger.info('Starting watcher...')
    asyncio.run(watcher(interval=10, wait=5))
