class LLMDebater:
    """
    A class that facilitates a debate between 2 LLMs to propose and analyse possible solutions
    """

    def __init__(self):
        self.generator_persona = ''
        self.discriminator_persona = ''

        self.conversation_history = []

    def generate_response(self, role: str, context: str, message: str) -> str:
        """
        Structured method to call the LLM and return a response
        """
        prompt = f"Role: {role}\n\n{context}\n\n{message}\nResponse:"
        
        response = openai.ChatCompletion.acreate(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": role}, {"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"].strip()

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

        message = "Start the discussion by proposing a solution."
        for round_num in range(max_rounds):
            # LLM 1 proposes a solution
            response1 = self.generate_response(self.persona1, problem_statement, message)
            self.conversation_history.append({"role": "LLM1", "content": response1})
            
            # LLM 2 critiques and refines the solution
            response2 = self.generate_response(self.persona2, problem_statement, f"Critique: {response1}\nRefine the solution.")
            self.conversation_history.append({"role": "LLM2", "content": response2})
            
            # Update the message for the next round
            message = f"Refined solution so far: {response2}\nFurther improve or debate this."

        return self.conversation_history

def main():
    api_key = "your_openai_api_key"
    debater = LLMDebater(api_key)

    traffic_data = {
        "high_accident_zones": ["Junction A", "Highway B"],
        "congestion_patterns": {"8AM-10AM": "Heavy on Route X", "5PM-7PM": "Severe on Highway Y"}
    }
    
    graph_context = "Graph of roads, intersections, and congestion data."

    result = debater.debate(traffic_data, graph_context, max_rounds=3)
    
    for entry in result:
        print(f"{entry['role']}: {entry['content']}\n")


if __name__=='__main__':
    main()