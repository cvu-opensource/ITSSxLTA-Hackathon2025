import os
from pathlib import Path
from dotenv import load_dotenv

import asyncio
import requests

import cv2
import numpy as np

from ultralytics import YOLO  # Using YOLOv8 for accident detection

load_dotenv()

# Load API endpoints
BACKEND_API = os.environ('BACKEND_API')

# Define models (replace with actual paths)
ACCIDENT_MODEL_PATH = "models/yolov8_accident.pt"
accident_model = YOLO(ACCIDENT_MODEL_PATH)  # temp

"""
Loading video feed for CV
"""

def load_live_videos():
    """Extracts live Singapore highway camera feed using LTA website"""
    
    LTA_API = "https://api.data.gov.sg/v1/transport/traffic-images"
    response = requests.get(LTA_API).json()

    current_timestamp, cameras = response['items'][0]['timestamp'], response['items'][0]['cameras']

    for idx, camera in enumerate(cameras):
        print(idx, camera)

    return None  # TODO: Replace with actual live video source


def load_simulated_videos():
    """Loads simulation videos from a folder"""
    video_folder = r"test_videos"
    return sorted(Path(video_folder).rglob('*.mp4'))


def extract_frames(video_source, target_fps=5):
    """Extracts frames from a video dynamically based on target FPS"""
    cap = cv2.VideoCapture(video_source)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)  # Original FPS
    frame_interval = int(frame_rate / target_fps)  # Skip frames accordingly
    frames = []

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % frame_interval == 0:  # Control FPS
            frames.append(frame)

        frame_count += 1
    
    cap.release()
    return frames

"""
Accident detection
"""

async def detect_accidents(frames):
    """Runs accident detection model on extracted frames"""
    results = []
    for frame in frames:
        # Run model on frame (change to video?)
        results.append(accident_model(frame))

        # Simulate async processing delay
        await asyncio.sleep(0.1)

    return results

async def send_accident_updates(accident_results):
    """Sends accident detection results to backend"""
    for result in accident_results:

        # TODO: Format this later on
        data = {"location": "Highway X", "status": "Accident Detected", "confidence": result.conf}
        requests.post(BACKEND_API + '/api/accidents', json=data)

        # Prevent rate limit issues
        await asyncio.sleep(0.1)

"""
Traffic flow detection
"""

def analyze_traffic_flow(video_source):
    """Uses Optical Flow to detect traffic movement"""
    cap = cv2.VideoCapture(video_source)
    ret, prev_frame = cap.read()
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    flow_data = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        avg_speed = np.mean(magnitude)  # Average movement speed

        flow_data.append(avg_speed)
        prev_gray = gray
    
    cap.release()
    return flow_data

async def send_traffic_updates(flow_data):
    """ Sends traffic flow data to backend """
    avg_traffic_speed = np.mean(flow_data)
    congestion_level = "High" if avg_traffic_speed < 1.0 else "Low"

        # TODO: Format this later on
    data = {"location": "Highway X", "traffic_speed": avg_traffic_speed, "congestion": congestion_level}
    requests.post(BACKEND_API + '/api/traffic', json=data)
    
    # Prevent rate limit issues
    await asyncio.sleep(0.1)

"""
Main pipeline
"""

async def main_pipeline(target_fps=5):
    """Runs the entire CV pipeline"""
    print("🚀 Starting Traffic Monitoring Pipeline...")

    # Load videos
    videos = load_simulated_videos()
    # videos = load_live_videos()

    for video in videos:
        print(f"Processing video: {video}")

        # Extract frames dynamically
        frames = extract_frames(video, target_fps=target_fps)

        # Run Accident Detection
        accident_results = await detect_accidents(frames)

        # Run Traffic Flow Analysis
        flow_data = analyze_traffic_flow(video)

        # Send data to backend
        await asyncio.gather(
            send_accident_updates(accident_results),
            send_traffic_updates(flow_data)
        )


if __name__ == "__main__":
    asyncio.run(main_pipeline(target_fps=5))
