# Import required packages
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

data = pd.read_csv('Clustering.csv', header=None, names=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'])
data.head()

continuous_features = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
data[continuous_features].describe()
data.head()
mms = MinMaxScaler()
mms.fit(data)
data_transformed = mms.transform(data)
Sum_of_squared_distances = []
k_means = [*range(2, 15)]
for k in k_means:
    km = KMeans(n_clusters=k)
    km = km.fit(data_transformed)
    Sum_of_squared_distances.append(km.inertia_)

plt.plot(k_means, Sum_of_squared_distances, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum_of_squared_distances')
plt.title('Elbow Method For Optimal k')
plt.show()