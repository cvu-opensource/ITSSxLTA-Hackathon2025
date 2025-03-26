import os
from dotenv import load_dotenv
import json
import requests
import pickle

load_dotenv()
# print('os.environ', os.environ)


class LLMDebater:
    """
    A class that facilitates a debate between 2 LLMs to propose and analyse possible solutions
    """

    def __init__(self):
        self.model_url = "http://localhost:7000/api/chat"

        self.generator_persona = 'Urban Traffic Engineer, focusing on finding the most effective, cost-effective and quick solutions.'
        self.discriminator_persona = 'AI Traffic Analyst, emphasizing efficiency, safety, and long-term sustainability of proposed plans.'

        self.conversation_history = []

    def generate_response(self, role: str, context: str, message: str) -> str:
        """
        Structured method to call the LLM and return a response
        """
        context = context.replace("'", "")
        prompt = f"Your role is: {role}\n\nThis is the context: {context}\n\nDo this: {message}\nResponse:"
        # prompt = prompt[:100]
        # print("prompt", prompt)
        # print('\n\n\n\n\ JSON!!!!!!!!!!!!!', json.dumps({
        #             "model": "deepseek-r1:1.5b",
        #             "messages": [
        #                 {"role": "user", "content": prompt}
        #             ],
        #             "temperature": 0.7}))
        response = requests.post(
            self.model_url,
            data=json.dumps({
                "model": "deepseek-r1:1.5b",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                # "temperature": 0.7,
                "stream": False,
                }),
            timeout=10  # Set timeout for better handling
        )
        # print(eval(response.content.decode('utf-8')))
        response.raise_for_status()
        response_dict = eval(response.content.decode('utf-8').replace('true', 'True'))
        response = response_dict['message']['content'].split('</think>')[-1]

        return response
        # except Exception as e:
        #     return f"Error communicating with local model: {e}"
        

    def debate(self, traffic_data, graph_context, max_rounds=3):
        """
        Orchestrates a structured debate between two LLMs
        
        Args:
            traffic_data [dict]: Dict containing accident and congestion records
            graph_context [str]: String representation of the traffic network graph
            max_rounds [int]: Maximum number of debate rounds
            
        Returns:
            List of conversation exchanges.
        """
        # Format the initial problem statement
        problem_statement = (
            f"Traffic Data: {traffic_data}\n\n"
            f"Graph Context: {graph_context}\n\n"
            "Discuss and propose solutions to reduce accident rates and traffic congestion in the network."
        )
        specifications = 'Keep your responses clear and concised, always following a structured manner.'
        message = "Start the discussion by proposing a solution to reduce traffic congestion and accidents in the proposed region."

        for round_num in range(max_rounds):
            # LLM 1 proposes a solution
            response1 = self.generate_response(self.generator_persona, problem_statement, message + specifications)

            self.conversation_history.append({"role": "LLM1", "content": response1})
            # print('response1', response1)
            # LLM 2 critiques and refines the solution
            message = f'An {self.generator_persona} created this solution. Critique and refine it: {response1}\n'
            response2 = self.generate_response(self.discriminator_persona, problem_statement, message + specifications)
            self.conversation_history.append({"role": "LLM2", "content": response2})
            
            # Update the message for the next round
            message = f"Refined solution so far: {response2}\nFurther improve or debate this."
            # print('response2', response2)
        return self.conversation_history

def main():
    debater = LLMDebater()

    received_data = [
        {
            "location": "TPE(PIE) - Exit 2 to Loyang Ave",
            "average_pixel_speed": 4.6e-05,
            "average_traffic_density": 0.0,
            "average_vehicles": 6.0,
            "accidents": {"2025-03-25T22:15:53"},
        },
        {
            "location": "TPE(PIE) - Tampines Viaduct",
            "average_pixel_speed": 8.3e-05,
            "average_traffic_density": 0.0,
            "average_vehicles": 8.0,
            "accidents": {"2025-03-25T22:15:53"},
        },
        {
            "location": "Tanah Merah Coast Road towards Changi",
            "average_pixel_speed": 4.7e-05,
            "average_traffic_density": 0.0,
            "average_vehicles": 5.0,
            "accidents": {"2025-03-25T20:05:48", "2025-03-25T23:10:36"},
        },
        {
            "location": "TPE (PIE) - Upper Changi F/O",
            "average_pixel_speed": 6.5e-05,
            "average_traffic_density": 0.0,
            "average_vehicles": 3.666667,
            "accidents": {
                "2025-03-25T22:40:54",
                "2025-03-25T23:05:55",
                "2025-03-25T22:50:35",
                "2025-03-25T23:00:35",
                "2025-03-25T23:15:56",
            },
        },
        {
            "location": "TPE(PIE) - Entrance to PIE from Tampines Ave 10",
            "average_pixel_speed": 6.8e-05,
            "average_traffic_density": 0.0,
            "average_vehicles": 7.0,
            "accidents": {
                "2025-03-25T22:40:54",
                "2025-03-25T23:05:55",
                "2025-03-25T22:50:35",
                "2025-03-25T23:00:35",
                "2025-03-25T23:15:56",
            },
        },
        {
            "location": "TPE(SLE) - TPE Exit KPE",
            "average_pixel_speed": 7.4e-05,
            "average_traffic_density": 0.0,
            "average_vehicles": 9.333333,
            "accidents": {
                "2025-03-25T22:40:54",
                "2025-03-25T23:05:55",
                "2025-03-25T22:50:35",
                "2025-03-25T23:00:35",
                "2025-03-25T23:15:56",
            },
        },
        {
            "location": "TPE(PIE) - Entrance from Tampines FO",
            "average_pixel_speed": 3.3e-05,
            "average_traffic_density": 0.0,
            "average_vehicles": 3.333333,
            "accidents": {
                "2025-03-25T22:40:54",
                "2025-03-25T23:05:55",
                "2025-03-25T22:50:35",
                "2025-03-25T23:00:35",
                "2025-03-25T23:15:56",
            },
        },
        {
            "location": "TPE(SLE) - On rooflp of Blk 189A Rivervale Drive 9",
            "average_pixel_speed": 0.000105,
            "average_traffic_density": 1.6e-05,
            "average_vehicles": 9.333333,
            "accidents": {
                "2025-03-25T22:40:54",
                "2025-03-25T23:05:55",
                "2025-03-25T22:50:35",
                "2025-03-25T23:00:35",
                "2025-03-25T23:15:56",
            },
        },
        {
            "location": "TPE(PIE) - Seletar Flyover",
            "average_pixel_speed": 5.9e-05,
            "average_traffic_density": 0.0,
            "average_vehicles": 10.666667,
            "accidents": {
                "2025-03-25T22:40:54",
                "2025-03-25T23:05:55",
                "2025-03-25T22:50:35",
                "2025-03-25T23:00:35",
                "2025-03-25T23:15:56",
            },
        },
        {
            "location": "TPE(SLE) - LP790F (On SLE Flyover)",
            "average_pixel_speed": 5.1e-05,
            "average_traffic_density": 0.0,
            "average_vehicles": 6.0,
            "accidents": {
                "2025-03-25T22:40:54",
                "2025-03-25T23:05:55",
                "2025-03-25T22:50:35",
                "2025-03-25T23:00:35",
                "2025-03-25T23:15:56",
            },
        },
    ]

    graph_context = "Graph of roads, intersections, and congestion data."

    result = debater.debate(received_data, graph_context, max_rounds=5)
    
    for entry in result:
        print(f"{entry['role']}: {entry['content']}\n")


if __name__=='__main__':
    main()
