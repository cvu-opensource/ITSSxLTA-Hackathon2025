from fastapi import FastAPI
from debater import LLMDebater
import pickle
from visualize_graph import TrafficGraph

# Initialise app and classes
app = FastAPI()
llmdebater = LLMDebater()

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

[{'role': 'LLM1', 'content': '\n\nTo address traffic congestion and accident rates across the region, a structured approach focusing on optimizing road design, enhancing occupancy management, reducing visibility factors, and improving safety protocols can lead to significant improvements. Here are key strategies:\n\n1. **Optimize Road Design and Construction:**\n   - Introduce smart materials like smart lanes or adaptive signal systems to enhance visibility.\n   - Incorporate new infrastructure such as temporary roads or green spaces in areas prone to congestion.\n\n2. **Enhance Road Occupancy Management:**\n   - Implement traffic signals at high-流量 areas to manage congestion effectively.\n   - Use real-time data tracking and predictive analytics for better capacity management.\n\n3. **Reduce Accidents through Traffic Hazard Management:**\n   - Focus on specific areas with known traffic hazards, such as potholes or construction zones, by increasing safety measures and visibility.\n   - Develop emergency response plans to ensure rapid actuation during potential accidents.\n\n4. **Improve Safety Protocols:**\n   - Establish clear accident reporting mechanisms for all incidents.\n   - Train drivers in hazard awareness, stopping signals, and emergency procedures.\n\nBy addressing these areas, traffic congestion can be minimized while reducing the incidence of accidents, ensuring a safer urban environment.'}, {'role': 'LLM2', 'content': '\n\n**Final Answer: Optimizing Traffic Safety Measures**\n\nTo address the increasing traffic accidents, here are structured strategies focused on road design, occupancy management, hazard prevention, and safety protocols:\n\n1. **Optimize Road Design and Construction**\n   - **Introduce Smart Materials:** Replace standard lanes with smart lanes equipped with adaptive signal systems or smart lights to enhance visibility.\n   - **Implement Temporary Roads:** Construct temporary roads in areas prone to congestion during peak hours for temporary solutions.\n   - **Green Spaces:** Incorporate green spaces such as shaded pedestrian areas to manage traffic flow.\n\n2. **Enhance Road Occupancy Management**\n   - **Traffic Signals at High-Flow Areas:** Establish fixed or adaptive traffic signal systems at high-流量 roads to manage congestion effectively.\n   - **Real-Time Analytics:** Use predictive analytics to anticipate peak flows and adjust signal timings dynamically for better capacity management.\n\n3. **Reduce Accidents through Traffic Hazard Management**\n   - **Targeted Safety Measures:** Focus on areas with known traffic hazards, such as potholes or construction zones. Enhance visibility by adding lights or using adaptive signals.\n   - **Emergency Response Plans:** Develop clear accident reporting and response protocols to ensure quick action during potential incidents.\n\n4. **Improve Safety Protocols**\n   - **Accident Reporting:** Implement a formal report system for all accidents, including those reported at unexpected times of high traffic flow.\n   - **Driver Training:** Train drivers in hazard awareness, stopping signals, and emergency procedures to prevent accidents.\n\n**Conclusion:**\nBy addressing these areas, we aim to create a safer urban environment.'}, {'role': 'LLM1', 'content': '\n\nTo address the increasing traffic accidents and reduce traffic congestion in the network, here are structured strategies focused on road design, occupancy management, hazard prevention, and safety protocols:\n\n### 1. **Optimize Road Design and Construction**\n   - **Introduce Smart Materials:** Replace standard lanes with smart lanes equipped with adaptive signal systems or smart lights to enhance visibility.\n   - **Implement Temporary Roads:** Construct temporary roads in areas prone to congestion during peak hours for temporary solutions.\n   - **Green Spaces:** Incorporate green spaces such as shaded pedestrian areas to manage traffic flow.\n\n### 2. **Enhance Road Occupancy Management**\n   - **Traffic Signals at High-Flow Areas:** Establish fixed or adaptive traffic signal systems at high-流量 roads to manage congestion effectively.\n   - **Real-Time Analytics:** Use predictive analytics to anticipate peak flows and adjust signal timings dynamically for better capacity management.\n\n### 3. **Reduce Accidents through Traffic Hazard Management**\n   - **Targeted Safety Measures:** Focus on areas with known traffic hazards, such as potholes or construction zones. Enhance visibility by adding lights or using adaptive signals.\n   - **Emergency Response Plans:** Develop clear accident reporting and response protocols to ensure quick action during potential incidents.\n\n### 4. **Improve Safety Protocols**\n   - **Accident Reporting:** Implement a formal report system for all accidents, including those reported at unexpected times of high traffic flow.\n   - **Driver Training:** Train drivers in hazard awareness, stopping signals, and emergency procedures to prevent accidents.\n\n### Conclusion:\nBy addressing these areas, we aim to create a safer urban environment. Further improvement or debate this. Keep your responses clear and concise, always following a structured manner.'}, {'role': 'LLM2', 'content': '\n\n**Strategies for Reducing Traffic Accidents and Congestion: A Comprehensive Approach**\n\n**1. Road Design:**\n   - **Introduce Smart Lanes with Adaptive Signals:** Enhance traffic flow by integrating smart lanes that use adaptive signal systems to manage traffic effectively.\n   - **Construct Temporary Roads During Peak Hours:** Handle congestion temporarily to prevent permanent increases in accidents due to reduced road capacity.\n   - **Use Green Spaces for Pedestrian Management:** Create shaded areas to manage pedestrian traffic and reduce overall congestion.\n\n**2. Road Occupancy Management:**\n   - **Establish Fixed or Adaptive Traffic Signals at High-Flow Areas:** Optimize signal timings to efficiently handle high volumes, reducing accidents caused by reduced visibility.\n   - **Use Real-Time Analytics for Optimized Signal Timings:** Analyze current traffic patterns to adjust signals in real-time, ensuring smoother transitions and reduced accident rates.\n\n**3. Traffic Hazard Management:**\n   - **Target Safety Measures in Traffic Zone:** Address specific traffic hazard zones (e.g., potholes) by enhancing visibility through smart materials or lights.\n   - **Develop Clear Accident Reporting Mechanisms:** Establish systems for quick reporting to prompt immediate action during incidents, reducing panic and potential safety risks.\n\n**4. Safety Protocols:**\n   - **Implement a Formal Accident Report System:** Develop procedures for documenting accidents with detailed information on injuries, behavior, and solutions.\n   - **Driver Training in Hazard Awareness, Stopping Signals, and Crisis Management:** Provide training to ensure safe interactions, reducing the likelihood of accidents and improving overall safety.\n\n**5. Stakeholder Coordination:**\n   - Collaborate with local authorities, departments responsible for road design, traffic management, and emergency services to align strategies.\n   - Share updated data on traffic flow, congestion levels, and accident rates to make informed decisions.\n\nBy integrating these strategies, we can enhance both road efficiency and safety, ultimately reducing both traffic congestion and the likelihood of accidents.'}, {'role': 'LLM1', 'content': '\n\n**Comprehensive Strategy for Reducing Traffic Accidents and Congestion**\n\nTo address traffic congestion and accident rates in the region, we propose an integrated strategy that combines smart lane design with adaptive signal systems, optimized traffic signal timings, targeted traffic hazard management, safety protocols, stakeholder coordination, and clear reporting mechanisms.\n\n1. **Smart Lane Design:**\n   - **Introduce Smart Lanes:** Enhance traffic flow by integrating smart lanes using adaptive signals to manage congestion effectively.\n   - **Implement Real-Time Analytics:** Use systems to adjust signal timings in real-time based on current conditions, ensuring smoother traffic transitions.\n\n2. **Optimize Traffic Signal Timings:**\n   - **Real-Time Reporting:** Develop a formal accident report system for quick information sharing and response during incidents.\n   - **Driver Training:** Train drivers in safety awareness, stopping signals, and crisis management to prevent accidents from escalating.\n\n3. **Target Safety Measures:**\n   - **Address Safety Zones:** Focus on specific areas like potholes or traffic hazards (e.g., Traffic Hazard) by improving visibility with smart materials or lights.\n   - **Clear Reporting Mechanisms:** Establish systems for quick reporting of incidents to prompt immediate action, reducing panic and safety risks.\n\n4. **Formal Accident Reporting System:**\n   - Create a unified system for documenting accidents across the region, ensuring transparency and accountability.\n\n5. **Integration of Systems:**\n   - Combine smart lane design with traffic signal optimization since smart lanes handle surface flow, while signals influence that within the surface area.\n   - Optimize signals to potentially influence other variables indirectly, such as accident rates through smoother transitions.\n\n6. **Stakeholder Involvement:**\n   - Involve local authority to ensure decisions are aligned with region needs.\n   - Share traffic data and congestion levels across all areas for informed decision-making.\n\n7. **Testing and Adjustment:**\n   - Test smart lane implementation during peak hours to assess effectiveness in reducing congestion.\n   - Gradually integrate traffic signal optimization as more data becomes available, ensuring responsiveness to changes.\n\n**Conclusion:**\nThis strategy is holistic, addressing multiple variables influencing both flow and congestion. By integrating smart lanes with adaptive signals, optimized signal timings, targeted safety measures, formal accident reporting, stakeholder coordination, and real-time data sharing, we aim for a comprehensive approach that ensures overall safety and efficiency in the region.'}, {'role': 'LLM2', 'content': "\n\nTo effectively reduce traffic accidents and congestion, a comprehensive and integrated strategy is necessary. Here's a structured plan based on the thought process:\n\n1. **Smart Lane Design**: \n   - Implement smart lanes to adjust signal timings in real-time as traffic conditions change (heavy or light). This allows drivers to react quickly, potentially saving time instead of stopping all cars.\n   - Consider integrating smart lights with adaptive signals specifically designed for safety zones where visibility is an issue.\n\n2. **Adaptive Signals**:\n   - Use real-time data from cameras and sensors in smart lanes to optimize signal timings based on traffic flow and conditions. This ensures dynamic adjustments to manage congestion efficiently.\n\n3. **Driver Training**:\n   - Provide comprehensive training programs that include crash avoidance techniques, understanding of road signs, and emergency response skills.\n   - Focus on developing safe driving norms through crash assessments, ensuring drivers are familiar with expected accident outcomes.\n\n4. **Safety Zones**:\n   - Use smart materials for visibility improvement in specific areas like potholes or traffic hazards. Test these materials under controlled conditions before real-world implementation.\n   - Integrate smart lights to adjust signal timing based on actual conditions (green or red) to reduce accidents caused by poor visibility.\n\n5. **Accident Reporting System**:\n   - Develop a formal reporting system with multiple layers, from local reports through national levels as needed. This ensures accountability and transparency in incidents.\n\n6. **Integration of Systems**:\n   - Combine smart lane design with adaptive signals for real-time adjustments to flow management. Optimize signal timings based on traffic sensor data and real-time conditions.\n   - Use phased implementation, starting with smart lanes or adaptive signals initially, then gradually adding more as data becomes available.\n\n7. **Stakeholder Involvement**:\n   - Involve traffic engineers, government officials, and local communities in planning and decision-making processes to ensure buy-in from all levels.\n   - Organize regular meetings with stakeholders to discuss progress and address concerns early.\n\n8. **Testing Across Areas**:\n   - Conduct tests across different regions to identify effective strategies in specific areas, adjusting plans as needed based on localized success or failure.\n\nBy integrating these elements through a phased approach, the strategy aims to create a holistic solution that reduces congestion, improves safety, and integrates technology for better monitoring and response."}, {'role': 'LLM1', 'content': "\n\nTo address the issue of reducing traffic accidents and congestion in the region, a comprehensive multi-step strategy is essential. Here's how each solution can be implemented effectively:\n\n1. **Smart Lane Design**: Introduce real-time monitoring using traffic cameras to assess road flow. This allows drivers to change lanes faster when conditions demand, potentially reducing congestion.\n\n2. **Adaptive Signals**: Implement real-time signal changes that reflect current traffic conditions. Change signals more frequently than regular stops but less often than full stops to optimize efficiency.\n\n3. **Driver Training**: Provide comprehensive training covering crash prevention techniques and emergency response skills. Ensure continuous updating based on driver feedback and experience.\n\n4. **Safety Zones**: Use smart materials in safety zones, testing them under controlled conditions before deployment to avoid risks of implementation.\n\n5. **Accident Reporting System (ARS)**: Develop a clear ARS with levels for local, national, and international reporting. This ensures comprehensive tracking and quick identification of patterns.\n\n6. **Integration of Systems**: Combine smart lane changes with adaptive signal updates based on real-time data. Smart lanes adjust to traffic flow changes, while signals optimize timing based on sensor data.\n\n7. **Stakeholder Involvement**: Engage engineers, officials, and communities in planning and implementation. Conduct regular meetings for progress updates and problem-solving.\n\n8. **Testing Across Areas**: Conduct regional tests to ensure strategies work locally before implementing across the region.\n\n**Implementation Strategy**:\n\n- **Phased Adoption**: Introduce smart lane changes first, then adaptive signals, followed by training programs, safety zones, and ARS testing.\n  \n- **Clear Communication**: Regular check-ins with stakeholders, including local representatives, can help manage any issues promptly.\n\n- **Multi-Level Reporting**: Ensure all levels of reporting (local, national, international) are in place to track accidents and report issues effectively.\n\nBy following this structured approach, the region can achieve a reduction in both traffic congestion and accident rates through practical, informed solutions."}, {'role': 'LLM2', 'content': '\n\n**Refined Traffic Safety Strategy Plan**\n\n1. **Smart Lane Design:**\n   - Introduce real-time monitoring using traffic cameras and sensors.\n   - Gradually increase lane adjustments based on current road conditions, optimizing flow faster when needed.\n\n2. **Adaptive Signals:**\n   - Implement signal changes more frequently than full stops but less often than stops to optimize timing.\n   - Use dynamic sensors for real-time adjustments without requiring manual intervention.\n\n3. **Driver Training Program:**\n   - Offer comprehensive training programs with continuous updates based on driver feedback and experience.\n   - Engage stakeholders in training sessions to ensure effectiveness.\n\n4. **Safety Zones:**\n   - Temporarily allocate areas to reduce congestion but prioritize safety by considering local events or sudden changes.\n\n5. **Integrated Traffic Hazard Management:**\n   - Consider causal relationships between traffic hazards and other variables, possibly integrating automated systems for better management.\n\n6. **Multi-Phase Implementation:**\n   - Implement smart lane design first, followed by adaptive signals, then training, safety zones, and ARS testing in small areas before scaling up.\n\n7. **Feedback and Review:**\n   - Conduct regular reviews with stakeholders to address issues promptly and make adjustments as needed.\n   - Foster community engagement through collaborative planning and transparent communication.\n\nThis strategy balances real-time data, comprehensive coverage, and community involvement to enhance traffic safety effectively.'}, {'role': 'LLM1', 'content': '\n\n**Revised Traffic Safety Strategy Plan**\n\n1. **Smart Lane Design:**\n   - Implement real-time monitoring using LIDAR or AI for precise lane predictions.\n   - Adjust lanes dynamically to optimize flow without waiting for full-scale changes.\n\n2. **Adaptive Signal Systems:**\n   - Use micro-sensors and dynamic adjustment systems to manage vehicle movement efficiently, reducing congestion where possible.\n\n3. **Driver Training Program:**\n   - Offer targeted training in both general skills and specialized areas based on real-time data from smart lane design.\n   - Differentiate between high-risk drivers for personalized instruction.\n\n4. **Safety Zones with Localized Analysis:**\n   - Temporarily reduce traffic congestion in specific, localized areas to ensure quick adjustments without affecting the rest of the network.\n\nThis revised plan prioritizes variables with higher causal factors (e.g., road occupancy, traffic flow) and incorporates predictive analytics and localized feedback loops for real-time optimization. It also ensures that training is targeted and personalized based on data from integrated smart lane systems.'}, {'role': 'LLM2', 'content': '\n\n**Revised Traffic Safety Strategy Plan:**\n\n1. **Smart Lane Design:**\n   - Implement real-time monitoring using advanced LIDAR sensors or AI-driven predictive analytics to detect and predict traffic flow patterns in real time.\n   - Use dynamic lane adjustment algorithms that predict the need for additional lanes based on vehicle behavior data collected from real-world measurements (e.g., using smart camera technology).\n   - Optimize lane adjustments based on historical traffic data, adjusting predictions when new road capacity changes or environmental conditions evolve.\n\n2. **Adaptive Signal Systems:**\n   - Introduce micro-sensor technologies in vehicles that monitor pedestrian crossings, traffic lights, and pedestrian movements.\n   - Design adaptive signal systems with dynamic coordination of traffic lights to ensure optimal flow during congestion while minimizing disruptions to pedestrian safety.\n   - Use machine learning models to predict traffic patterns based on historical data and real-time sensor inputs, adjusting signal timings accordingly.\n\n3. **Driver Training Program:**\n   - Develop targeted driver training programs that focus on skills identified by smart lane design and adaptive signal systems.\n   - Utilize gamified learning platforms or simulations that provide personalized training experiences for drivers at different risk levels (e.g., high-risk drivers who rarely drive normally versus regular drivers).\n   - Train in a real-world setting with immediate feedback from the smart lane system, allowing drivers to adjust their behavior based on real-time data.\n\n4. **Safety Zones with Localized Analysis:**\n   - Establish " Safety Zones" where traffic congestion is minimized for specific intersections or road segments identified by localized analysis of traffic patterns.\n   - Use AI-driven tools to identify areas with higher than average traffic volumes and implement temporary measures (e.g., reduced speed limits, curbside lane operations) during peak hours or on certain days.\n\n5. **Cost-Effectiveness and Scalability:**\n   - Evaluate the cost of implementing advanced technologies (e.g., LIDAR sensors, AI models for adaptive signals) and compare it with existing infrastructure costs.\n   - Optimize training programs by considering the potential return on investment from reduced accidents or improved road safety.\n\n**Rationale:**  \nThe revised plan prioritizes variables with higher causal factors (e.g., traffic occupancy, road flow) and integrates predictive analytics and localized feedback loops for real-time optimization. It also emphasizes personalized training based on data from integrated smart lane systems to ensure targeted interventions where they are most needed.'}]
