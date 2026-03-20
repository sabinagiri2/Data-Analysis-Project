import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Load your Excel file
df = pd.read_excel("checked_file.xlsx")  # Replace with your actual file path

# Select and clean the data
data = df[['C1', 'C2', 'C3', 'C4']].dropna()

# Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

# Compute inertia for a range of k values
inertia = []
k_range = range(1, 11)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(scaled_data)
    inertia.append(kmeans.inertia_)

# Plot the Elbow curve
plt.plot(k_range, inertia, marker='o')
plt.title("Elbow Method")
plt.xlabel("Number of clusters (k)")
plt.ylabel("Inertia")
plt.grid(True)
plt.show()

# Estimate the elbow point using second derivative
inertia_diff = np.diff(inertia)
inertia_diff2 = np.diff(inertia_diff)
optimal_k = np.argmin(inertia_diff2) + 2  # +2 due to second derivative and 0-indexing
print(f"Estimated optimal number of clusters: {optimal_k}")
