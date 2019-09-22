__author__ = 'BR'

"""
Author: BIKASH ROY

File name: elbowmethod.py
"""

'''
This python program is used to find the knee of 
Squared_sum_error to K-means in a plot.
'''
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

# Read the data from the file,
# If there is no header, name them.
data = pd.read_csv('Clustering.csv', header=None, names=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'])
data.head()
data[['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']].describe()
print(len(data))
mms = MinMaxScaler()
mms.fit(data)
data_transformed = mms.transform(data)
print(len(data_transformed))
Sum_of_squared_distances = []
k_means = [*range(2, 22, 2)]
for k in k_means:
    km = KMeans(n_clusters=k)
    km = km.fit(data_transformed)
    Sum_of_squared_distances.append(km.inertia_)

# plt.plot(k_means, Sum_of_squared_distances, 'bx-')
# plt.xlabel('k')
# plt.ylabel('Sum_of_squared_distances')
# plt.title('Elbow Method For Optimal k')
# plt.show()