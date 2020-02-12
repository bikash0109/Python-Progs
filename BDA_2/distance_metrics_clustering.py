__author__ = 'BR'

"""
Author: BIKASH ROY

File name: distance_metrics_clustering.py

This is a program to plot the 3 distance metrics clustering
dendrogramns.
"""


import matplotlib.pyplot as plt
import pandas as pd
'exec(%matplotlib inline)'
import numpy as np
import scipy.cluster.hierarchy as shc

df = pd.read_csv('cities.csv')
data = df.iloc[:, 2:10].values
names = ['BOS', 'NY', 'DC', 'MIA', 'CHI', 'SEA', 'SF', 'LA', 'DEN']
linked = shc.linkage(data, 'single')
plt.figure(figsize=(10, 7))
plt.title("Single Linkage Cluster")
shc.dendrogram(linked,
            orientation='top',
            distance_sort='descending',
            labels=names,
            show_leaf_counts=True)
plt.show()

linked = shc.linkage(data, 'complete')
plt.figure(figsize=(10, 7))
plt.title("Complete Linkage Cluster")
shc.dendrogram(linked,
            orientation='top',
            distance_sort='descending',
            show_leaf_counts=True,
            labels=names)
plt.show()

linked = shc.linkage(data, 'average')
plt.figure(figsize=(10, 7))
plt.title("Average Linkage Cluster")
shc.dendrogram(linked,
            orientation='top',
            distance_sort='descending',
            show_leaf_counts=True,
            labels=names)
plt.show()