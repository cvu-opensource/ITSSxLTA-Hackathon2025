from pyvis.network import Network
import networkx as nx
import pickle

fp = '/mnt/e/XTraffic/causal_analysis/globalcausal/district_DAG_lambda_0.001_rho_1_K_2.pkl'
with open(fp, 'rb') as file: 
    E_est, G_est = pickle.load(file)


accidents = [0, 1, 2, 3, 4, 5, 6, 7]
meta = [8, 9, 10, 11, 12, 13, 14],
outcomes = [15, 16, 17]

column_text_mapping = {
    0: '1125-Traffic Hazard',
    1: '1183-Trfc Collision-Unkn Inj',
    2: '1182-Trfc Collision-No Inj',
    3: '1179-Trfc Collision-1141 Enrt',
    4: '20002-Hit and Run No Injuries',
    5: 'FIRE-Report of Fire',
    6: '1125A-Animal Hazard', 
    7: 'CZP-Assist with Construction',
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

orders = {
    3: meta,
    2: accidents,
    1: outcomes,
}
example_graph = E_est[0]
net = Network('5000px', '5000px')

graph = nx.DiGraph()

drawn_edges = set()
for idx, factor in column_text_mapping.items():
    for jdx in range(idx, max(column_text_mapping.keys())):
        if (idx, jdx) not in drawn_edges and (jdx, idx) not in drawn_edges:
            i_name = column_text_mapping[idx]
            j_name = column_text_mapping[jdx]

            for order, ls in orders.items():
                if idx in ls:
                    i_order = order
                if jdx in ls:
                    j_order = order
            
            if i_order > j_order:
                a, b = i_name, j_name
                a_idx, b_idx = idx, jdx
            elif j_order > i_order:
                a, b = j_name, i_name
                a_idx, b_idx = jdx, idx
            else:
                a, b = None, None

            if a is not None and b is not None:
                    weight = example_graph[a_idx][b_idx]
                
                # if weight > 0.001:
                    print('weight', weight)
                    print('a', a, 'b', b)
                    drawn_edges.add( (a, b) )
            # net.add_edge(idx, jdx, weight=weight)

net = Network(directed=True)

for idx, text in column_text_mapping.items():
    net.add_node(text)

for edge in drawn_edges:
    net.add_edge(edge[0], edge[1])

net.save_graph('mygraph.html')

print(drawn_edges)
# graph.add_edges_from(drawn_edges)
# nx.write_graphml(graph, 'my_graph.graphml')
# nt = Network('500px', '500px')
# populates the nodes and edges data structures
# nt.from_nx(graph)

# nt.show('nx.html', notebook=False)

# net.show('nx.html', notebook=False)
# net.save_graph('nx.html')