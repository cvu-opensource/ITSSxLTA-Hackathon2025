import os
import logging
from dotenv import load_dotenv

import asyncio
from httpx import AsyncClient
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import requests

# Get some hardcoded values 
from hardcode import camera_details, camera_mapping, weather_sensor_mapping

# Initialise DB
from Database import Database
db = Database()

# Configure logging format
logging.basicConfig(
    format="[%(asctime)s] %(message)s",  # Use %(asctime)s instead of %H:%M:%S
    datefmt="%H:%M:%S",  # Correct time formatting
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Environment variables
load_dotenv()
SUPABASE_API = os.environ.get("SUPABASE_API", "")
PLANNING_API = os.environ.get("PLANNING_API", "")

# FastAPI App
app = FastAPI()
http_client = AsyncClient()

"""
Handling websocket connections with UI for live updates each time update is received
"""

ui_clients = []
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Establish websocket client with UI clients"""
    await websocket.accept()
    ui_clients.append(websocket)
    try:
        while True:
            try:
                await asyncio.wait_for(websocket.receive_text(), timeout=30)
            except asyncio.TimeoutError:
                await websocket.send_text("ping")
                continue
    except WebSocketDisconnect as e:
        logger.error(f'Unable to establish websocket client due to {e}')
        ui_clients.remove(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        if websocket in ui_clients:
            ui_clients.remove(websocket)


async def broadcast(message: str):
    """Send message to all connected UI clients"""
    disconnected_clients = []
    for client in ui_clients:
        try:
            await client.send_text(message)
            logger.info('Data sent to client.')
        except Exception as e:
            logger.error(f'Unable to send data to websocket clients due to {e}')
            disconnected_clients.append(client)

    # Remove disconnected clients
    for client in disconnected_clients:
        ui_clients.remove(client)

"""
Handles processing of data between different services
"""

def get_weather_sensor_data():
    """
    Calls NEA API to get rainfall data across singapore
    """
    url = "https://api.data.gov.sg/v1/environment/rainfall"
    response = requests.get(url).json()

    readings = response['items'][0]['readings']
    readings = {station['station_id']:station['value'] for station in readings}

    stations = response['metadata']['stations']
    station_data = {
        station['id']: {
            'name': station['name'],
            'location': (station['location']['latitude'], station['location']['longitude']),
            'rainfall': readings[station['id']]
        } for station in stations
    }
    return station_data

def process_average_traffic_data(data):
    """
    Given n records of traffic data, compute the average and determine state of the most recent values
    """
    logger.info(f'data {data}')
    temp = {}
    for datetime, traffic_data in data.items():
        for k, v in traffic_data.items():
            temp[k] = temp.get(k, []) + [float(v)]

    logger.info(f'temp {temp}')
    result = {}
    for statistic in temp:
        if len(temp[statistic]) > 0:
            average = sum(temp[statistic]) / len(temp[statistic])
            result[statistic] = {
                'average': round(average, 6),
                'relative': round(temp[statistic][-1] / average, 3) if average > 0.0 else 0.0
            }
        else:
            result[statistic] = {
                'average': 0.0,
                'relative': 0.0
            }
    logger.info(f'result {result}')
    return result

def process_camera_data(camera_data):
    """
    Given a dictionary of camera data, add in hardcoded details for UI usage
    """
    for camera_id, data in camera_data.items():
        if camera_id in camera_details:
            data['angle'] = camera_details[camera_id]['angle']
            data['description'] = camera_details[camera_id]['description']
        else:
            data['angle'] =  0
            data['description'] = 'Road'
    return camera_data

def calculate_total_relative(statistics):
    """
    Calculates the sum of 'average_relative' values for a main key
    """
    total = 0
    for statistic in statistics.values():
        total += statistic['average_relative']
    return total

def priority_mapping(statistics):
    """
    Custom mapping of relative values to priority level
    """
    if len(statistics) > 0:
        average_relative_value = sum([statistic['average_relative'] for _, statistic in statistics.items()]) / len(statistics)
        if average_relative_value >= 1.5: 
            return 'High' 
        if average_relative_value >= 0.5:
            return 'Normal' 
    return 'Low'

def process_grouped_traffic_data(traffic_data):
    """
    Given n records of traffic data for different cameras, group cameras based on mapping,
    compute the average to determine priority based on relative values
    """
    grouped_data = {}
    for mapping, camera_ids in camera_mapping.items():
        temp = {}

        # For each mapping, extract all relative statistics from average traffic data regardless of sensor
        for camera_id in camera_ids:
            if camera_id in traffic_data:
                data = traffic_data[camera_id]
                for statistic, value in data.items():
                    temp[statistic] = temp.get(statistic, {'average': [], 'relative': []})
                    temp[statistic]['average'].append(float(value['average']))
                    temp[statistic]['relative'].append(float(value['relative']))

        # Convert extracted relative traffic data per sensor into one averaged value across sensors per mapping
        grouped_data[mapping] = {}
        for statistic in temp:
            grouped_data[mapping][statistic] = grouped_data[mapping].get(statistic, {})
            grouped_data[mapping][statistic]['average_average'] = round(sum(temp[statistic]['average']) / len(temp[statistic]['average']), 2)
            grouped_data[mapping][statistic]['average_relative'] = round(sum(temp[statistic]['relative']) / len(temp[statistic]['relative']), 2)

    # Sort mappings by averaged relative data
    grouped_data = sorted(
        grouped_data.items(),
        key=lambda item: calculate_total_relative(item[1]),
        reverse=True
    )
    
    # Converting back to dictionary and adding priority level
    grouped_data = {
        key: {
            **val,
            **{'priority': priority_mapping(val)}
        } for (key, val) in grouped_data
    }
    return grouped_data

def process_grouped_weather_data(grouped_data, weather_data):
    """
    Given groups of traffic sensors, weather data from different sensors and weather sensor mapping,
    combine average rainfall into grouped data
    """
    for area in grouped_data:
        rainfall_values = []
        for weather_sensor in weather_sensor_mapping[area]:
            rainfall_values.append(weather_data[weather_sensor]['rainfall'])
        if rainfall_values:
            grouped_data[area]['average_rainfall'] = round(sum(rainfall_values) / len(rainfall_values), 2)
        else:
            grouped_data[area]['average_rainfall'] = 0.0
    return grouped_data

"""
Handles API calls
"""

@app.get("/healthz")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}


async def save_cameras(cameras: dict):
    """
    Updates camera data in the database
    """
    try:
        # Necessary since json serialising and sending over data somehow converts the int key into a str
        cameras = {
            int(camera_id): data for camera_id, data in cameras.items()
        }
        cameras = process_camera_data(cameras)
        logger.info('Updating camera data in DB.')
        db.insert_cameras(cameras)
    except Exception as e:
        logger.error(f'Failed to save camera data with insert_cameras: {e}')
        return {'success': False, 'message': f'Database insert_cameras service unreachable due to {e}'}
    return {'success': True, 'message': 'Camera data successfully updated in DB service.'}


async def save_traffic_flow(results: dict):
    """
    Sends traffic flow updates to the database service for storage
    """
    try:
        logger.info(f'Saving traffic flow data {results}.')
        for camera_id, datas in results.items():
            for data in datas:
                db.insert_traffic_flows({camera_id: data})
    except Exception as e:
        logger.error(f'Error connecting to DB service to insert_traffic_flows: {e}')
        return {'success': False, 'message': f'Database insert_traffic_flows service unreachable due to {e}'}
    return {'success': True, 'message': 'Traffic data successfully sent to DB service.'}


async def save_images(images: dict):
    """
    Sends image data to the database service for storage
    """
    try:
        # Necessary since json serialising and sending over data somehow converts the int key into a str
        images = {
            int(camera_id): data for camera_id, data in images.items()
        }
        logger.info('Saving new traffic images.')
        db.insert_images(images)
    except Exception as e:
        logger.error(f'Error connecting to DB service to insert_images: {e}')
        return {'success': False, 'message': f'Database insert_images service unreachable due to {e}'}
    return {'success': True, 'message': 'Image data successfully sent to DB service.'}


@app.post("/traffic_update")
async def receive_traffic_update(data: dict):
    """
    Receives live traffic updates from the CV service and broadcasts them to UI clients and DB service
    """
    try:
        logger.info('Received CV-traffic update.')

        # Save updates to db
        await save_cameras(data['cameras'])
        await save_traffic_flow(data['results'])
        await save_images(data['frames'])

        # Send update to all UI clients
        await broadcast(data)

        logger.info('Completed CV-traffic update.')
        return {'success': True, 'message': 'Traffic update processed'}
    except Exception as e:
        logger.error(f'Error processing traffic updates due to {e}.')
        return {'success': False, 'message': f'Error processing traffic updates due to {e}'}


@app.get("/get_all_data")
async def get_all_data():
    """
    Fetches traffic data from database service when UI client refreshes map page
    """
    result = {}
    # Get all camera data
    logger.info('Retrieving camera data.')
    try: 
        camera_data = db.get_all_cameras()
        camera_data = process_camera_data(camera_data)
    except Exception as e:
        logger.error(f'Error connecting to DB service for get_all_cameras: {e}')
        return {'success': False, 'message': f'Database service unreachable due to {e}'}
    
    logger.info('Retrieving image and traffic data.')
    for camera_id in camera_data:
        result[int(camera_id)] = {'camera_data': camera_data[int(camera_id)]}

        # Get traffic data per sensor
        data = {'lta_camera_id': int(camera_id), 'n': 20}
        try:
            traffic_data = db.get_traffic_flow_by_sensor_last_n(data)

            # Compute average and relative values for traffic data before sending to UI
            result[int(camera_id)]['traffic_data'] = process_average_traffic_data(traffic_data)

        except Exception as e:
            logger.error(f'Error connecting to DB service for get_traffic_flow_by_sensor_last_n: {e}')
            return {'success': False, 'message': f'Database service unreachable due to {e}'}
    
        # Get latest image data per sensor
        data = {'lta_camera_id': int(camera_id)}
        try:
            result[int(camera_id)]['image_data'] = db.get_image(data)
        except Exception as e:
            logger.error(f'Error connecting to DB service for get_traffic_flow_by_sensor_last_n: {e}')
            return {'success': False, 'message': f'Database service unreachable due to {e}'}
    return result


@app.get("/get_camera_data_by_sensor")
async def get_camera_data_by_sensor(camera_id):
    """
    Fetches camera data from database service for a specific sensor to create pin in UI
    """
    try: 
        data = {'lta_camera_id': camera_id}
        camera_data = db.get_camera(data)
        return process_camera_data({int(camera_id): camera_data})
    except Exception as e:
        logger.info(f'Error retrieving camera data for camera {camera_id}: {e}')
        return {'success': False, 'message': f'Error retrieving camera data for camera {camera_id}: {e}'}


@app.get("/get_traffic_data_by_sensor")
async def get_traffic_data_by_sensor(camera_id):
    """
    Fetches traffic data from database service for a specific sensor to update pin popup in UI
    """
    try: 
        data = {'lta_camera_id': camera_id, 'n': 10}
        traffic_data = db.get_traffic_flow_by_sensor_last_n(data)
        return process_average_traffic_data(traffic_data)
    except Exception as e:
        logger.info(f'Error retrieving traffic data for camera {camera_id}: {e}')
        return {'success': False, 'message': f'Error retrieving traffic data for camera {camera_id}: {e}'}


@app.get('/get_live_traffic_updates')
async def get_live_traffic_updates():
    """
    Fetches traffic data from database service when UI client refreshes dashboard page
    """
    # Get all camera data
    logger.info('Retrieving camera data for live traffic updates.')
    try: 
        camera_data = db.get_all_cameras()
    except Exception as e:
        logger.error(f'Error connecting to DB service for get_all_cameras: {e}')
        return {'success': False, 'message': f'Database service unreachable due to {e}'}
    
    result = {}
    logger.info('Retrieving traffic data for live traffic updates.')
    for camera_id in camera_data:

        # Get traffic data per sensor
        data = {'lta_camera_id': camera_id, 'n': 20}
        try:
            traffic_data = db.get_traffic_flow_by_sensor_last_n(data)
            
            # Compute average and relative values for traffic data first
            result[camera_id] = process_average_traffic_data(traffic_data)

        except Exception as e:
            logger.error(f'Error connecting to DB service for get_traffic_flow_by_sensor_last_n: {e}')
            return {'success': False, 'message': f'Database service unreachable due to {e}'}
        
    logger.info('Grouping traffic data for live traffic updates.')
    result = process_grouped_traffic_data(result)

    logger.info('Getting weather data for live traffic updates.')
    weather_data = get_weather_sensor_data()

    logger.info('Grouping weather and traffic data for live traffic updates.')
    result = process_grouped_weather_data(result, weather_data)
    return result


@app.post("/get_recommendations")
async def get_recommendations():
    """
    Sends data to the predictive analysis service from db and returns response to UI
    """
    areas = ['TPE', 'KPE', 'PIE']
    logger.info('Retrieving all sensors from db for recommendations.')
    
    try:
        camera_datas = db.get_all_cameras()
        camera_datas = process_camera_data(camera_datas)
    except Exception as e:
        logger.info(f'Error retrieving traffic flow for recommendations data due to {e}')
        return {'success': False, 'message': f'Error retrieving camera data for recommendations: {e}'}
    
    # Only get data for sensors within specified areas
    data = {}
    for area in areas:
        for camera_id in camera_mapping[area]:
            camera_data = camera_datas[camera_id]

            logger.info(f'Retrieving traffic flow data for camera-{camera_id} from db for recommendations.')
            try:
                data = {'lta_camera_id': camera_id, 'n': 1000}
                traffic_flow_data = db.get_traffic_flow_by_sensor_last_n(data)
            except Exception as e:
                logger.info(f'Error retrieving traffic flow data for recommendations due to {e}')
                return {'success': False, 'message': f'Error retrieving traffic flow data for recommendations: {e}'}

            logger.info(f'Retrieving accident data for camera-{camera_id} from db for recommendations.')
            try:
                data = {'lta_camera_id': camera_id, 'n': 1000}
                accident_data = db.get_accidents_by_sensor_last_n(data)
            except Exception as e:
                logger.info(f'Error retrieving accident data for recommendations due to {e}')
                return {'success': False, 'message': f'Error retrieving accident data for recommendations: {e}'}
            
            data[int(camera_id)] = {
                'camera_data': camera_data,
                'traffic_flow': traffic_flow_data,
                'accident_data': accident_data
            }

    logger.info(f'Sending data to retrieve recommendations. {data}')
    try:
        async with AsyncClient() as client:
            response = await client.post(PLANNING_API + '/get_planning_recommendations', json=data)
            return response.json()
    except Exception as e:
        logger.info(f'Error retrieving planning recommendations due to {e}')
        return {'success': False, 'message': f'Error retrieving planning recommendations: {e}'}
