import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, fcluster

# Load your Excel file
df = pd.read_excel("checked_file.xlsx")  # Replace with your actual file path

# Select and clean the data
data = df[['C1', 'C2', 'C3', 'C4']].dropna()

# Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

# Perform hierarchical clustering (Ward's method)
linked = linkage(scaled_data, method='ward')

# Calculate silhouette scores for a range of k values
silhouette_scores = []
k_range = range(2, 11)

for k in k_range:
    labels = fcluster(linked, k, criterion='maxclust')
    score = silhouette_score(scaled_data, labels)
    silhouette_scores.append(score)

# Plot the Silhouette Scores
plt.plot(k_range, silhouette_scores, marker='o')
plt.title("Silhouette Method (Hierarchical Clustering)")
plt.xlabel("Number of clusters (k)")
plt.ylabel("Silhouette Score")
plt.grid(True)
plt.show()

# Estimate the optimal k as the one with highest silhouette score
optimal_k = k_range[np.argmax(silhouette_scores)]
print(f"Estimated optimal number of clusters: {optimal_k}")
