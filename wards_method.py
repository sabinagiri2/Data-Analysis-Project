# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 22:41:43 2025

@author: Apana Ale
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster


# Load the data
file_path =r"finaltable.xlsx"  # Replace with your file path
data = pd.read_excel(file_path, sheet_name="Sheet1")

# Extract relevant columns (C1, C2, C3, C4)
cluster_data = data[['C1', 'C2', 'C3', 'C4']]

# Drop rows with missing/infinite values (or impute them)
cluster_data_clean = cluster_data.dropna()  # Removes rows with NaN
cluster_data_clean = cluster_data_clean.replace([np.inf, -np.inf], np.nan).dropna()  # Handles inf

#  Perform hierarchical clustering (Ward's method)
Z = linkage(cluster_data_clean, method='ward')

# Plot the dendrogram
plt.figure(figsize=(15, 8))
plt.title('Hierarchical Clustering Dendrogram (Ward Linkage)')
plt.xlabel('Sample Index')
plt.ylabel('Distance (Ward)')
dendrogram(
    Z,
    truncate_mode='lastp',
    p=10,
    show_leaf_counts=True,
    leaf_rotation=90.,
    leaf_font_size=8.,
)
plt.axhline(y=100, color='r', linestyle='--', label='Cutoff for 2 clusters')
plt.legend()
plt.show()

# Cut the dendrogram to get 2 clusters
clusters = fcluster(Z, t=4, criterion='maxclust')

#  Add cluster labels to the cleaned data
cleaned_data_with_clusters = data.loc[cluster_data_clean.index].copy()
cleaned_data_with_clusters['Cluster'] = clusters

#  Print cluster distribution
print("\nCluster Distribution:")
print(cleaned_data_with_clusters['Cluster'].value_counts())

#  Print mean values per cluster
print("\nMean Values per Cluster:")
print(cleaned_data_with_clusters.groupby('Cluster')[['C1', 'C2', 'C3', 'C4']].mean())