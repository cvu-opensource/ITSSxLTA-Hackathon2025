from pyvis.network import Network
import networkx as nx
import pickle
from matplotlib import pyplot as plt
import math
import numpy as np
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class TrafficGraph():
    """
    Parses a numpy array and some user-defined dictionaries into a graph.
    """
    def __init__(self):  # nope all g
        """
        Instantiates nx.DiGraph and adds nodes. Edges are added later so we can threshold the weights.

        Args:
            - hierarchies: dictionary mapping an informative, to an integer representing a certain graph order.
                there are 4 elements: list of indexes, colours, x and y of the starting node. # TODO finalize this
        """
        self.graph = nx.DiGraph()

        self.for_drawing_naming = {
            'Traffic Hazard': 'Traffic\n Hazard',
            'Collisions (Injuries)': 'Collision\n Inj',
            'Collisions (No Injuries)': 'Collision\n No Inj',
            'Collisions Enrt': 'Collision\n Enrt',
            'Hit and Run (No Injuries)': 'Hit and Run\n No Inj',
            'Reported Fire': 'Reported\n Fire',
            'Animal Hazard': 'Animal\n Hazard', 
            'Road flow': 'Road\n flow',
            'Road occupancy': 'Road\n occupancy',
            'Road speed': 'Road\n speed',
        }

        factors = {
            0: 'Traffic Hazard',
            1: 'Collisions (Injuries)',
            2: 'Collisions (No Injuries)',
            3: 'Collisions Enrt',
            4: 'Hit and Run (No Injuries)',
            5: 'Reported Fire',
            6: 'Animal Hazard', 
            7: 'Construction',
            8: 'Weekday',
            9: 'Event_days',
            10: 'Visibility',
            11: 'Surface',
            12: 'Terrain',
            13: 'Width',
            14: 'Weather',
            15: 'Road flow',
            16: 'Road occupancy',
            17: 'Road speed',
        }
        self.idx_to_factor = factors
        self.factor_to_idx = {v: k for k, v in factors.items()}

        # list of indices -> keys in the column_text_mapping dict
        accidents = [0, 1, 2, 3, 4, 5, 6, 7]
        meta = [8, 9, 10, 11, 12, 13, 14]
        outcomes = [15, 16, 17]
        self.hierarchies = {
            3: (meta, 'green', 1, 5),
            2: (accidents, 'red', 1, 3),
            1: (outcomes, 'blue', 1, 1),
        }
        self.num_factors = len(factors)

        for idx, text in self.idx_to_factor.items():
            for order, (ls, colour, x, y) in self.hierarchies.items():
                if idx in ls:
                    nth = ls.index(idx)
                    x_node = x + nth
                    y_node = y

            # print('x y text', x_node, y_node, text)
            self.graph.add_node(
                text,
                pos=(x_node, y_node)
            )

        self.general_options = {"edgecolors": "tab:grey", "node_size": 1200, 'node_shape':'s'}
        self.pos = nx.get_node_attributes(self.graph,'pos')


    def add_edges(self, network: np.ndarray, weight_thresh: float):
        weights_dict, thresh_edges = self.get_dag_edges(network, weight_thresh)
        edges_weights = [(edge[0], edge[1], weights_dict[edge]) for edge in thresh_edges]
        self.graph.add_weighted_edges_from(edges_weights)


    def vis_digraph(self, network: np.ndarray, save_path: str, weight_thresh=0.1, dash_thresh=0.5):
        assert isinstance(network, np.ndarray), 'Assertion failed, network passed in is not a numpy array!'
        assert network.shape[0] == self.num_factors, f'Assertion failed, network passed in does not match the expected dimension given by the factor graph! Expected {self.num_factors}, got {network.shape[0]}'
        assert len(network.shape) == 2, 'Assertion failed, network recieved is not a 2d array.'

        weights, to_draw_edges = self.get_dag_edges(network, weight_thresh)
        self.draw_nodes()
        self.draw_edges(to_draw_edges=to_draw_edges, weights=weights, dash_thresh=dash_thresh)

        plt.savefig(save_path)
        plt.clf()

    def get_context_for_llm(self, 
                            query_nodes: list,
                            weight_threshs: list | None = None,
                            top_n: int = 3,) -> str:
        """
        Given a query (list of query nodes), call query_graph to retrieve subgraphs
        then, format it into a string to pass to an llm as context
        """
        context_string = "Context: For traffic accidents in this region, "
        graphs, pyvis_networks = self.query_graph(query_nodes, weight_threshs, top_n)
        for graph in graphs:
            edge_attrs: dict = nx.get_edge_attributes(graph, 'weight')
            for pair, weight in edge_attrs.items():
                higher_order, lower_order = pair  # first item may not always be of a higher order, it just is
                # greater than or equal to the order of the lower_order variable. Oh well
                lower_order = lower_order.replace('\n', '')
                higher_order = higher_order.replace('\n', '')

                context_string += f"{higher_order} has a causal factor of {weight} with {lower_order}. "
        
        serial_box = []
        for idx, pyvis_network in enumerate(pyvis_networks):
            path = Path(f'temp_{idx}.html')
            full_path = path.resolve().name
            pyvis_network.save_graph(full_path)
            with open(full_path, 'rb') as file:
                file = file.read()
                serial = pickle.dumps(file)
            serial_box.append(serial)

        return context_string, serial_box
        

    def query_graph(self,
                    query_nodes: list,
                    weight_threshs: list | None = None,
                    top_n: int = 3,
        ) -> tuple[list[nx.Graph], list[Network]]:
        """
        Queries graphs and returns subgraphs with edges beyond a certain threshold and only the top_n.
        The graphs returned will be a directed graph for similar order sorting as the source graph,
        to preserve hierarchical information.
        """
        subgraphs = []
        if weight_threshs is None:
            weight_threshs = [0.1] * len(query_nodes)

        for q, w_t in zip(query_nodes, weight_threshs):
            assert q in self.factor_to_idx, 'Assertion failed, recieved a query for a node that does not exist!'
            subg = nx.DiGraph() #Create subgraph
            subg.add_node(q)
            # generate lists of (higher_order, lower_order, weight), depending on if
            children_with_weights = [(q, child, self.graph[q][child].get('weight')) for child in self.graph.neighbors(q) 
                                    if self.graph[q][child] is not None and self.graph[q][child].get('weight') > w_t]
            
            parents_with_weights = [(parent, q, self.graph[parent][q].get('weight')) for parent in self.graph.predecessors(q)
                                    if self.graph[parent][q].get('weight') is not None and self.graph[parent][q].get('weight') > w_t]
            
            children_with_weights.extend(parents_with_weights)
            all_relations = children_with_weights
            # Sort the neighbors based on the edge weight in descending order and return the top `n`
            top_n_neighbors = sorted(all_relations, key=lambda x: x[2], reverse=True)[:top_n]

            for higher_order, lower_order, weight in top_n_neighbors:
                subg.add_edge(higher_order, lower_order, weight=weight)
            subgraphs.append(subg)

        nets = []
        for subgraph in subgraphs:
            net = Network()
            net.from_nx(subgraph)
            nets.append(net)
        return subgraphs, nets


    def draw_nodes(self):
        for order, (ls, colour, x, y) in self.hierarchies.items():
            texts = [self.idx_to_factor[i] for i in ls]
            labels = {}
            for text in texts:
                if text in self.for_drawing_naming:
                    label = self.for_drawing_naming[text]
                else:
                    label = text
                labels[text] = label
            nx.draw_networkx_nodes(self.graph, self.pos, nodelist=texts, node_color=f"tab:{colour}", **self.general_options)
            nx.draw_networkx_labels(self.graph, self.pos, labels=labels, font_size=8)
            

    def draw_edges(self, to_draw_edges: list, weights:dict[tuple[int, int], float], dash_thresh=0.5):

        edge_weights = []
        edge_weights.extend([(edge, weights[edge]) for edge in to_draw_edges])

        for edge, weight in edge_weights:
            source_edge = edge[0]
            source_edge_idx = self.factor_to_idx[source_edge]
            for order, (ls, colour, _, _) in self.hierarchies.items():
                if source_edge_idx in ls:
                    edge_color = colour

            if weight > dash_thresh:
                style = 'solid'
            else:
                style = 'dashed'
            nx.draw_networkx_edges(
                self.graph,
                self.pos,
                edgelist=[edge],
                width=1,
                alpha=max(weight, 0.25),
                style=style,
                edge_color=f"tab:{edge_color}",
            )


    def get_dag_edges(self, network: np.ndarray, weight_thresh: float) -> tuple[dict[tuple, float], list]:
        """
        Get the edges into a set. Threshold by weight_thresh variable. Also returns a weight dictionary because we love you
        """
        weights = {}
        thresh_edges = set()
        for idx, factor in self.idx_to_factor.items():  # O(N^2)! i love!
            for jdx in range(idx, self.num_factors):
                if (idx, jdx) not in thresh_edges or (jdx, idx) not in thresh_edges:
                    i_name = self.idx_to_factor[idx]
                    j_name = self.idx_to_factor[jdx]

                    for order, (ls, colour, _, _) in self.hierarchies.items():
                        if idx in ls:
                            i_order = order
                        if jdx in ls:
                            j_order = order
                    # i love logic! yes i am lazy to come up with better logic. please file an issue if this greatly displeases you. i will not be checking the issues.
                    if i_order > j_order:
                        a, b = i_name, j_name
                        a_idx, b_idx = idx, jdx
                    elif j_order > i_order:
                        a, b = j_name, i_name
                        a_idx, b_idx = jdx, idx
                    else:
                        a, b = None, None

                    if a is not None and b is not None:
                        weight = network[a_idx][b_idx]
                        
                        if weight > weight_thresh:
                            thresh_edges.add( (a, b) )
                            weights[(a, b)] = weight

        thresh_edges = list(thresh_edges)
        return weights, thresh_edges


# Intitialise global variables first (no matter the usage)
with open(os.environ.get('PICKLE_FILE'), 'rb') as file: 
    E_est, G_est = pickle.load(file)  # dict, dict

location_key_mappings = {
    0: 'PIE',
    1: 'CTE',
    2: 'AYE',
    3: 'TPE',
    4: 'BKE',
    5: 'ECP',
    6: 'KJE',
    7: 'SLE',
    8: 'KPE',
    9: 'MCE',
    10: 'Woodlands_Checkpoint',
    11: 'Tuas_Checkpoint',
    12: 'Sentosa',

}

# Converting E_est:dict to have sg_location keys
for key, sg_location in location_key_mappings.items():
    looped_key = key % 3  # TODO: change this once graph for all expressways are created
    E_est[sg_location] = E_est[looped_key]

# Dust out old integer pointers
[E_est.pop(key) for key in list(E_est.keys()) if isinstance(key, int)]

# Create graph dictionary any time this file is called
GRAPHS = {}
for key, network in E_est.items():
    graph = TrafficGraph()
    graph.add_edges(network, weight_thresh=0.1) 
    GRAPHS[key] = graph


# Simulate graph creation
# if __name__=='__main__':

    # keys_of_est = list(E_est.keys())
    # for key in keys_of_est:
    #     looped_key = key % 3
    #     sg_location = location_key_mappings[looped_key]
    #     E_est[sg_location] = E_est[looped_key]
        # E_est.pop(key)

    # simulating a query 

# query = ['PIE', ['Surface', 'Visibility', 'Traffic Hazard']]
# selected_graph = GRAPHS[query[0]]
# print(selected_network)

# graph = TrafficGraph()
# graph.add_edges(selected_network, weight_thresh=0.1)
# thing = selected_graph.get_context_for_llm(query_nodes=query[1])
# print(thing)
# selected_graph.vis_digraph(E_est[query[0]], save_path=f'graph_0.png')