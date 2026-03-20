import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.preprocessing import StandardScaler
from openpyxl import load_workbook

# 1. Load the data
file_path = "checked_file.xlsx"  # Replace with your file path
data = pd.read_excel(file_path, sheet_name="Sheet1")

# 2. Extract relevant columns (C1, C2, C3, C4)
cluster_data = data[['C1', 'C2', 'C3', 'C4']]

# 3. Check for missing/infinite values
print("Missing values:\n", cluster_data.isnull().sum())
print("\nInfinite values:\n", np.isinf(cluster_data).sum())

# 4. Drop rows with missing/infinite values (or impute them)
cluster_data_clean = cluster_data.dropna()  # Removes rows with NaN
cluster_data_clean = cluster_data_clean.replace([np.inf, -np.inf], np.nan).dropna()  # Handles inf

# 5. Standardize the data (after cleaning)
#scaler = StandardScaler()
#scaled_data = scaler.fit_transform(cluster_data_clean)
scaled_data = cluster_data_clean

# 6. Perform hierarchical clustering (Ward's method)
Z = linkage(scaled_data, method='ward')

# 7. Plot the dendrogram
plt.figure(figsize=(15, 8))
plt.title('Hierarchical Clustering Dendrogram (Ward Linkage)')
plt.xlabel('Sample Index')
plt.ylabel('Distance (Ward)')
dendrogram(
    Z,
    truncate_mode='lastp',
    p=20,
    show_leaf_counts=True,
    leaf_rotation=90.,
    leaf_font_size=8.,
)
plt.axhline(y=15, color='r', linestyle='--', label='Cutoff for 4 clusters')
plt.legend()
plt.show()

# 8. Cut the dendrogram to get 2 clusters
clusters = fcluster(Z, t=2, criterion='maxclust')

# 9. Add cluster labels to the cleaned data
cleaned_data_with_clusters = data.loc[cluster_data_clean.index].copy()
cleaned_data_with_clusters['Cluster'] = clusters

# 10. Print cluster distribution
print("\nCluster Distribution:")
print(cleaned_data_with_clusters['Cluster'].value_counts())

# 11. Print mean values per cluster
print("\nMean Values per Cluster:")
print(cleaned_data_with_clusters.groupby('Cluster')[['C1', 'C2', 'C3', 'C4']].mean())

from sklearn.metrics import silhouette_score
score = silhouette_score(scaled_data, clusters)



# 12. Add cluster numbers to the original Excel file
# First, reload the original Excel file to avoid data loss
original_data = pd.read_excel(file_path, sheet_name="Sheet1")

# Create a copy of the original and update only the rows used in clustering
original_data.loc[cluster_data_clean.index, 'Cluster'] = clusters

# Load the workbook and write back to the same sheet
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    original_data.to_excel(writer, index=False, sheet_name='Sheet1')

print(f"\nCluster labels have been added to the original file: {file_path}")
