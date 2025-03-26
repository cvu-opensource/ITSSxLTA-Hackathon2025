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
    10: 'vis',
    11: 'surface',
    12: 'terrain',
    13: 'width',
    14: 'weather',
    15: 'flow',
    16: 'occupancy',
    17: 'speed',
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
    # TODO: Geraldina here is the pseudocode
    sg_location: str = data['location']
    query_nodes: list[str] = data['query_nodes']
    selected_graph = graphs[sg_location]
    graph_context_string = selected_graph.get_context_for_llm(query_nodes=query_nodes)


    # Generate traffic data as LLM context
    processed_traffic_data = process_traffic_data(data)

    # Start debate and get debate history back
    history = llmdebater.debate(processed_traffic_data, graph_context_string, max_rounds=5)

    return history

@app.get('/healthz')
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy (healthy core bro is literally healthy if there was a health competition bro wold be first place bro eats health for dinner bro's middle name is health bro is fitness incarante bro years for the health mines)"}