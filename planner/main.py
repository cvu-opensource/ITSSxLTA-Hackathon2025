from fastapi import FastAPI
from debater import LLMDebater

# Initialise app and classes
app = FastAPI()
llmdebater = LLMDebater()


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
        processed_data['average_pixel_speed'] = all_data['traffic_data']['pixel_speed']['average']
        processed_data['average_traffic_density'] = all_data['traffic_data']['traffic_density']['average']
        processed_data['average_vehicles'] = all_data['traffic_data']['num_vehicles']['average']

        # Get unique accident times for each sensor location
        for accident in all_data['accident_data']:
            processed_data['accidents'] = processed_data.get('accidents', set())
            processed_data['accidents'].add(accident['datetime'])

        processed_datas.append(processed_data)
    return processed_datas


@app.get('/get_planning_recommendations')
def get_planning_recommendations(data):
    """
    Main planning recommendation service
    """
    # TODO: Generate graph as LLM context
    graph_data = ''

    # Generate traffic data as LLM context
    processed_traffic_data = process_traffic_data(data)

    # Start debate and get debate history back
    history = llmdebater.debate(processed_traffic_data, graph_data, max_rounds=5)

    return history

@app.get('/healthz')
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}