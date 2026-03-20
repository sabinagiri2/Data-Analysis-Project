# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 12:10:42 2025

@author: Apana Ale
"""

import pandas as pd
import matplotlib.pyplot as plt

# Load your data
file_path = r"checked_file.xlsx"
df = pd.read_excel(file_path)

# List of independent variables
x_vars = ['V106', 'V024', 'V025', 'V130', 'V131', 'V190', 'V701', 'V704',
          'SECOREG', 'SDIST', 'V001', 'V002', 'V003']

# Loop through each variable
for var in x_vars:
    # Create cross-tabulation
    ct = pd.crosstab(df['Cluster'], df[var])

    # Plot
    ct.T.plot(kind='bar', stacked=True, figsize=(10, 6))
    plt.title(f"Distribution of {var} by Cluster")
    plt.xlabel(var)
    plt.ylabel("Count")
    plt.legend(title='Cluster', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()