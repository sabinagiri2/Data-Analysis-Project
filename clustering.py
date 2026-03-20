import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

# Step 1: Load the dataset
df = pd.read_excel('cleaned_weights.xlsx')

# Step 2: Select the features for tree clustering
X = df[['WEIGHT1', 'WEIGHT2','WEIGHT3', 'WEIGHT4']]

# Step 3: Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 4: Perform hierarchical clustering
linked = linkage(X_scaled, method='ward')  # 'ward' keeps clusters compact

# Step 5: Plot the dendrogram
plt.figure(figsize=(10, 7))
dendrogram(linked,
           orientation='top',
           distance_sort='descending',
           show_leaf_counts=True)
plt.title('Hierarchical Clustering Dendrogram (Tree Form)')
plt.xlabel('Sample Index')
plt.ylabel('Distance')
plt.grid(True)
plt.show()
