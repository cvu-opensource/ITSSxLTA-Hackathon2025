import os
from dotenv import load_dotenv

from fastapi import FastAPI
from debater import LLMDebater
import pickle
from visualize_graph import GRAPHS

# Initialise app and classes
load_dotenv
app = FastAPI()
llmdebater = LLMDebater(os.environ.get('DEEPSEEK_API'))

# Test data 
try:
    from test_data import TPE, CTE, BKE, ECP, AYE, PIE, KJE, SLE, KPE, MCE, Woodlands_Checkpoint, Tuas_Checkpoint, Sentosa
except Exception as e:
    print(f'Unable to import test_data due to {e}')


def process_traffic_data(traffic_data):
    """
    Helper function to process traffic and image data before passing to respective functions
    """
    processed_datas = []
    for camera_id, all_data in traffic_data.items():
        processed_data = {}

        # Get location information
        processed_data['location'] = all_data['camera_data']['description']

        # Get traffic flow information
        processed_data['average_pixel_speed'] = all_data['traffic_data']['average_pixel_speed']
        processed_data['average_traffic_density'] = all_data['traffic_data']['average_traffic_density']
        processed_data['average_vehicles'] = all_data['traffic_data']['average_vehicles']

        # Get unique accident times for each sensor location
        for accident in all_data['traffic_data']['accidents']:
            processed_data['accidents'] = processed_data.get('accidents', set())
            processed_data['accidents'].add(accident)

        processed_datas.append(processed_data)
    return processed_datas


@app.get('/get_planning_recommendations')
def get_planning_recommendations(data):
    """
    Main planning recommendation service
    """
    # Extract other params from request for graphs
    sg_location: str = data['location']
    query_nodes: list[str] = data['query_nodes']
    selected_graph = GRAPHS[sg_location]
    graph_context_string = selected_graph.get_context_for_llm(query_nodes=query_nodes)

    # Generate traffic data as LLM context
    processed_traffic_data = process_traffic_data(data['traffic_data'])

    # Start debate and get debate history back
    history = llmdebater.debate(processed_traffic_data, graph_context_string, max_rounds=5)

    return history

@app.get('/healthz')
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy (healthy core bro is literally healthy if there was a health competition bro wold be first place bro eats health for dinner bro's middle name is health bro is fitness incarante bro years for the health mines)"}


# Test implementation
if __name__=='__main__':
    # Data to simulate call from backend service
    fake_data = {
        'traffic_data': TPE,  # TODO: change this as u need
        'location': 'TPE',   # TODO: and this too
        'query_nodes': ['surface', 'visibility', 'Traffic\n Hazard']
    }
    print(get_planning_recommendations(fake_data))
