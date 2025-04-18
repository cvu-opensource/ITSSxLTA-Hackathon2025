import numpy as np
import pandas as pd
from MMDAG import multiDAG_functional, net_fpca
from sklearn.preprocessing import scale
import pickle

if __name__ == '__main__':
    h = {}
    T = 24
    rho = 1
    K = 2
    lambda1 = 0.001
    h[0] = np.load('district_3_DAGdata.npy')
    # print(thing.shape)
    # print(np.isnan(thing).any())
    # print(h[0].shape)
    # h[0] = h[0][~np.isnan(h[0])]
    # print(h[0].shape)
    h[0] = h[0].transpose(0, 2, 1)
    h[1] = np.load('district_4_DAGdata.npy')
    # print(thing.shape)
    # print(np.isnan(thing).any())
    h[1] = h[1].transpose(0, 2, 1)
    h[2] = np.load('district_7_DAGdata.npy')
    # print(thing.shape)
    # print(np.isnan(thing).any())
    h[2] = h[2].transpose(0, 2, 1)
    h[3] = np.load('district_8_DAGdata.npy')
    # print(thing.shape)
    # print(np.isnan(thing).any())
    h[3] = h[3].transpose(0, 2, 1)
    P_id = {}
    P_all = 18
    # print('h', h)
    for i in range(4):
        P_id[i] = range(P_all)
        scale_matrix = np.zeros_like(h[i], dtype=np.float64)
        for j in range(P_all):
            scale_matrix[:, j, :] = h[i][:, j, :] / np.std(h[i][:, j, :])
        h[i] = scale_matrix
    # print('h', h)
    print('h shapes', [v.shape for k, v in h.items()])
    print('K', K)
    a, v = net_fpca(h, K=K)
    print('a shape', [t.shape for k, t in a.items()])
    print('v shape', [t.shape for k, t in v.items()])
    E_est, G_est = multiDAG_functional(a.copy(), lambda1=lambda1, rho=rho, P_id=P_id, P_all=P_all, alpha_max=2, max_iter=1)
    file_name = f'/mnt/e/XTraffic/causal_analysis/globalcausal/district_DAG_lambda_{lambda1}_rho_{rho}_K_{K}.pkl'
    with open(file_name, 'wb') as file:
        pickle.dump((E_est, G_est), file)
