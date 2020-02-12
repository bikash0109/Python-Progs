__author__ = 'BR'

"""
Author: BIKASH ROY

File name: k-mean-elbow.py
"""

'''
This python program is used to find the knee of 
Squared_sum_error to K-means in a plot.
'''

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random as rd


class Kmeans_class:
    def __init__(self, dataset, K):
        self.dataset = dataset
        self.out_dict = {}
        self.Centroids = np.array([]).reshape(self.dataset.shape[1], 0)
        self.K = K
        self.m = self.dataset.shape[0]

    def process_centroid(self, dataset, K):
        i = rd.randint(0, dataset.shape[0])
        Centroid_temp = np.array([dataset[i]])
        for k in range(1, K):
            D = np.array([])
            for x in dataset:
                D = np.append(D, np.min(np.sum((x - Centroid_temp) ** 2)))
            prob = D / np.sum(D)
            cummulative_prob = np.cumsum(prob)
            r = rd.random()
            i = 0
            for j, p in enumerate(cummulative_prob):
                if r < p:
                    i = j
                    break
            Centroid_temp = np.append(Centroid_temp, [dataset[i]], axis=0)
        return Centroid_temp.T

    def cal_distances(self, n_iter):
        # randomly Initialize the centroids
        self.Centroids = self.process_centroid(self.dataset, self.K)
        # compute euclidian distances and assign clusters
        for n in range(n_iter):
            EuclidianDistance = np.array([]).reshape(self.m, 0)
            for k in range(self.K):
                tempDist = np.sum((self.dataset - self.Centroids[:, k]) ** 2, axis=1)
                EuclidianDistance = np.c_[EuclidianDistance, tempDist]
            C = np.argmin(EuclidianDistance, axis=1) + 1
            # adjust the centroids
            Y = {}
            for k in range(self.K):
                Y[k + 1] = np.array([]).reshape(2, 0)
            for i in range(self.m):
                Y[C[i]] = np.c_[Y[C[i]], self.dataset[i]]

            for k in range(self.K):
                Y[k + 1] = Y[k + 1].T
            for k in range(self.K):
                self.Centroids[:, k] = np.mean(Y[k + 1], axis=0)

            self.out_dict = Y

    def get_centroid_value(self):
        return self.out_dict, self.Centroids.T

    def SSE(self):
        sse = 0
        for k in range(self.K):
            sse += np.sum((self.out_dict[k + 1] - self.Centroids[:, k]) ** 2)
        return sse


dataset = pd.read_csv('Clustering.csv', header=None, names=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'])
dataset.head()
dataset[['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']].describe()

dataset = dataset.iloc[:, [0, 9]].values

SSE_array = np.array([])
for K in range(2, 22, 2):
    kmeans = Kmeans_class(dataset, K)
    kmeans.cal_distances(100)
    out_dict, Centroids = kmeans.get_centroid_value()
    sse = 0
    for k in range(K):
        sse += np.sum((out_dict[k + 1] - Centroids[k, :]) ** 2)
    SSE_array = np.append(SSE_array, sse)
K_array = np.arange(2, 22, 2)
plt.plot(K_array, SSE_array)
plt.xlabel('K')
plt.ylabel('SSE')
plt.title('K V/S SSE')
plt.show()
