import os
from dotenv import load_dotenv

from fastapi import FastAPI
from debater import LLMDebater
import pickle
from visualize_graph import TrafficGraph

# Initialise app and classes
load_dotenv
app = FastAPI()
llmdebater = LLMDebater(os.environ.get('DEEPSEEK_API'))

# TODO: Hi gerard i initialize a bunch of this stuff before initing my class. Kinda messy
# Got any ideas where i can park all this yap
fp = '/mnt/e/ITSSxLTA-Hackathon2025/planner/district_DAG_lambda_0.001_rho_1_K_2.pkl'
with open(fp, 'rb') as file: 
    E_est, G_est = pickle.load(file)  # dict, dict

# list of indices, keys in the column_text_mapping dict
accidents = [0, 1, 2, 3, 4, 5, 6, 7]
meta = [8, 9, 10, 11, 12, 13, 14]
outcomes = [15, 16, 17]

# TODO: Something about locations is here. I map it to the various indexes of the already built graphs, the looping thing I was talking about @ Gerard
location_key_mappings = {
    0: 'PIE',
    1: 'CTE',
    2: 'AYE',
}

# convert the dictionary E_est to have sg_location keys now. all bs
for key, sg_location in location_key_mappings.items():
    looped_key = key % len(E_est)
    E_est[sg_location] = E_est[looped_key]
list_of_keys = list(E_est.keys())
[E_est.pop(key) for key in list_of_keys if isinstance(key, int)] # dust out the old pointers

# mapping index to strings. The \n  is for formatting the graph i create because 
# very long text kinda makes it unreadable, so newline saves us there
column_text_mapping = {
    0: 'Traffic\n Hazard',
    1: 'Collision\n Inj',
    2: 'Collision\n No Inj',
    3: 'Collision\n Enrt',
    4: 'Hit and Run\n No Inj',
    5: 'Reported\n Fire',
    6: 'Animal\n Hazard', 
    7: 'Construction',
    8: 'weekday',
    9: 'event_days',
    10: 'visibility',
    11: 'surface',
    12: 'terrain',
    13: 'width',
    14: 'weather',
    15: 'Road\n flow',
    16: 'Road\n occupancy',
    17: 'Road\n speed',
}

# to define the causal order of the factors, the larger the key the higher the order.
# index 1 2 and 3 are metainfo for drawing stuff so just ignore
order_metas = {
    3: (meta, 'green', 1, 5),
    2: (accidents, 'red', 1, 3),
    1: (outcomes, 'blue', 1, 1),
}

graphs = {}
for key, network in E_est.items():
    graph = TrafficGraph(column_text_mapping, order_metas)
    graph.add_edges(network, weight_thresh=0.1) 
    graphs[key] = graph

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
    # TODO: Geraldina here is the pseudocode
    sg_location: str = data['location']
    query_nodes: list[str] = data['query_nodes']
    selected_graph = graphs[sg_location]
    graph_context_string = selected_graph.get_context_for_llm(query_nodes=query_nodes)

    # Generate traffic data as LLM context
    processed_traffic_data = process_traffic_data(data['traffic_data'])
    # print('processed_traffic_data', processed_traffic_data)

    # Start debate and get debate history back
    history = llmdebater.debate(processed_traffic_data, graph_context_string, max_rounds=5)

    return history

@app.get('/healthz')
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy (healthy core bro is literally healthy if there was a health competition bro wold be first place bro eats health for dinner bro's middle name is health bro is fitness incarante bro years for the health mines)"}


some_camera_data = {
    'camera_data': {
        'angle': 325,
        'description': 'TPE (PIE) - Upper Changi F/O'
    },
    'traffic_data': {
            "location": "TPE (PIE) - Upper Changi F/O",
            "average_pixel_speed": 0.051769,
            "average_traffic_density": 0.458262,
            "average_vehicles": 6.283333,
            "accidents": [
                "2025-03-26T10:35:42",
                "2025-03-26T03:25:46",
                "2025-03-26T03:10:45",
                "2025-03-26T03:20:46",
                "2025-03-26T03:55:47",
                "2025-03-26T01:30:41",
                "2025-03-26T02:10:43",
                "2025-03-26T01:56:02",
                "2025-03-26T01:10:40",
                "2025-03-26T02:35:44",
                "2025-03-25T23:05:55",
                "2025-03-26T10:15:41",
                "2025-03-26T03:35:46",
                "2025-03-26T09:45:40",
                "2025-03-26T03:05:45",
                "2025-03-26T10:20:41",
                "2025-03-26T03:45:47",
                "2025-03-26T02:45:44",
                "2025-03-26T02:00:42",
                "2025-03-26T01:50:42",
                "2025-03-26T02:40:44",
                "2025-03-25T22:40:54",
                "2025-03-26T09:20:39",
                "2025-03-26T09:31:00",
                "2025-03-26T02:05:43",
                "2025-03-26T09:26:00",
                "2025-03-26T02:15:43",
                "2025-03-26T02:25:43",
                "2025-03-26T10:25:42",
                "2025-03-26T09:56:01",
                "2025-03-26T03:30:46",
                "2025-03-26T01:05:40",
                "2025-03-26T10:45:42",
                "2025-03-26T03:50:47",
                "2025-03-26T09:40:40",
                "2025-03-26T01:40:42",
                "2025-03-26T02:30:44",
                "2025-03-26T10:06:01",
                "2025-03-26T01:25:41",
                "2025-03-26T10:31:02",
                "2025-03-26T10:40:42",
                "2025-03-26T09:36:00",
                "2025-03-26T10:01:01",
                "2025-03-26T09:10:59",
                "2025-03-26T01:45:42",
                "2025-03-25T23:15:56",
                "2025-03-26T10:51:02",
                "2025-03-25T23:00:35",
                "2025-03-26T02:55:45",
                "2025-03-26T01:20:41",
                "2025-03-26T03:15:45",
                "2025-03-26T10:10:41",
                "2025-03-26T01:35:41",
                "2025-03-25T22:50:35",
                "2025-03-26T02:20:43",
                "2025-03-26T03:40:46",
                "2025-03-26T00:50:40",
                "2025-03-26T03:00:45",
                "2025-03-26T02:50:44",
                "2025-03-26T09:51:00",
                "2025-03-26T09:15:59",
                "2025-03-26T00:56:00",
            ],
    }
}
fake_data = {
    'location': 'PIE', 
    'query_nodes': ['surface', 'visibility', 'Traffic\n Hazard'],
    'traffic_data': {
        7791: some_camera_data
    }
}
thing = get_planning_recommendations(fake_data)
print(thing)
