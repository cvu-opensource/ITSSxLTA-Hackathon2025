from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import json
import os
from httpx import AsyncClient
import redis.asyncio as redis
import logging


# Configure logging format
logging.basicConfig(
    format="[%(asctime)s] %(message)s",  # Use %(asctime)s instead of %H:%M:%S
    datefmt="%H:%M:%S",  # Correct time formatting
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# Database
SUPABASE_API = os.getenv("SUPABASE_API", "")

# Redis Cache Setup
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# FastAPI App
app = FastAPI()
http_client = AsyncClient()

"""
Handling websocket connections with UI for live updates each time update is received
"""

ui_clients = []

@app.websocket("/establish_websocket")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    ui_clients.append(websocket)
    try:
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30)
            except asyncio.TimeoutError:
                await websocket.send_text("ping")
                continue
    except WebSocketDisconnect:
        ui_clients.remove(websocket)

async def broadcast(message: str):
    """Send message to all connected UI clients"""
    for client in ui_clients:
        try:
            await client.send_text(message)
        except Exception as e:
            ui_clients.remove(client)  # Remove disconnected clients

"""
Handles processing of data between different services
"""

def process_average_traffic_data(data):
    """
    Given n records of traffic data, compute the average and determine state of the most recent values
    """
    temp = {}
    for datetime, traffic_data in data.items():
        for k, v in traffic_data.items():
            temp[k] = temp.get(k, []) + [v]

    result = {}
    for statistic in temp:
        average = round(sum(temp['statistic']) / len(temp['statistic']))
        result[statistic] = {
            'average': average,
            'relative': temp['statistic'][-1] / average
        }
    return result

"""
Handling API calls
"""

@app.get("/healthz")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}


async def save_traffic_flow(data: dict):
    """
    Sends traffic updates to the database service for storage
    """
    try:
        response = await http_client.post(SUPABASE_API + '/insert_traffic_flow', json=data)
        if response.status_code != 200:
            logger.info(f'Failed to save traffic data: {response.text}')
            return {'success': False, 'message': response.text}
    except Exception as e:
        logger.info(f'Error connecting to DB service: {e}')
        return {'success': False, 'message': f'Database service unreachable due to {e}'}

    # Send real-time update to UI clients
    await broadcast(json.dumps(data))

    return {'success': True, 'message': 'Traffic data successfully sent to DB service.'}

@app.websocket("/traffic_update")
async def receive_traffic_update(websocket: WebSocket):
    """
    Receives live traffic updates from the CV service and broadcasts them to UI clients and DB service
    """
    await websocket.accept()
    try:
        while True:
            response = await websocket.receive_text()
            data = json.dumps(response)
            logger.info('Received CV update.')

            # Save updates to db
            await save_traffic_flow(json.loads(data))

            # Send update to all UI clients
            await broadcast(data)
    except WebSocketDisconnect:
        logger.info('CV service disconnected.')


@app.get("/get_all_data")
async def get_all_data():
    """
    Fetches traffic data from database service when UI client refreshes
    """
    result = {}
    async with AsyncClient() as client:
        # Get all camera data
        try: 
            response = await client.post(SUPABASE_API + '/get_all_cameras')
            if response.status_code != 200:
                logger.info(f'Failed to retrieve camera data: {response.text}')
                return {'success': False, 'message': response.text}
            camera_data = response.json()
        except Exception as e:
            logger.info(f'Error connecting to DB service: {e}')
            return {'success': False, 'message': f'Database service unreachable due to {e}'}
        
        for camera_id in camera_data:
            result[camera_id] = {'camera_data': camera_data[camera_id]}

            # Get traffic data per sensor
            data = {'camera_id': camera_id, 'n': 10}
            try:
                response = await client.post(SUPABASE_API + '/get_traffic_flow_by_sensor_last_n', json=data)
                if response.status_code != 200:
                    logger.info(f'Failed to retrieve traffic data: {response.text}')
                    return {'success': False, 'message': response.text}
                traffic_data = response.json()

                # Compute average and relative values for traffic data before sending to UI
                result[camera_id]['traffic_data'] = process_average_traffic_data(traffic_data)

            except Exception as e:
                logger.info(f'Error connecting to DB service: {e}')
                return {'success': False, 'message': f'Database service unreachable due to {e}'}
            
            result['camera_id']


@app.get("/get_camera_data_by_sensor")
async def get_camera_data_by_sensor(camera_id):
    """
    Fetches camera data from database service for a specific sensor to create pin in UI
    """
    try: 
        async with AsyncClient() as client:
            data = {'camera_id': camera_id}
            response = await client.post(SUPABASE_API + '/get_camera', json=data)
            if response.status_code != 200:
                logger.info(f'Failed to retrieve camera data: {response.text}')
                return {'success': False, 'message': response.text}
            return response.json()
    except Exception as e:
        logger.info(f'Error retrieving camera data for camera {camera_id}: {e}')
        return {'success': False, 'message': f'Error retrieving camera data for camera {camera_id}: {e}'}


@app.get("/get_traffic_data_by_sensor")
async def get_traffic_data_by_sensor(camera_id):
    """
    Fetches traffic data from database service for a specific sensor to update pin popup in UI
    """
    try: 
        async with AsyncClient() as client:
            data = {'camera_id': camera_id}
            response = await client.post(SUPABASE_API + '/get_traffic_flow_by_sensor_last_n', json=data)
            if response.status_code != 200:
                logger.info(f'Failed to retrieve traffic data: {response.text}')
                return {'success': False, 'message': response.text}
            return response.json()
    except Exception as e:
        logger.info(f'Error retrieving traffic data for camera {camera_id}: {e}')
        return {'success': False, 'message': f'Error retrieving traffic data for camera {camera_id}: {e}'}

"""
COOKED APIS BRUH 
"""

@app.post("/predictive/analyze")
async def send_to_predictive_service(data: dict):
    """Sends data to the predictive analysis service."""
    response = await http_client.post("http://predictive-service/analyze", json=data)
    return response.json()
