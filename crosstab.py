import pandas as pd
import matplotlib.pyplot as plt

# Load your Excel file
file_path = r"clustered_output_1.xlsx"
df = pd.read_excel(file_path)

# List of independent variables
x_vars = ['V106', 'V024', 'V025', 'V130', 'V131', 'V190', 'V701', 'V704',
          'SECOREG', 'SDIST']

# Loop through each variable
for var in x_vars:
    # Create cross-tabulation of Cluster vs variable
    ct = pd.crosstab(df[var], df['Cluster'])  # x-axis var in rows, clusters in columns

    # Plot stacked bar chart
    ct.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='tab20c')

    # Plot styling
    plt.title(f"Cluster-wise Distribution of {var}")
    plt.xlabel(var)
    plt.ylabel("Count")
    plt.legend(title='Cluster', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
print(f"{var}: {df[var].notna().sum()} non-missing values")

