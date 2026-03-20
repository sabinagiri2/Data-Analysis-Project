# -*- coding: utf-8 -*-
"""
Created on Sat Jun 28 14:31:37 2025

@author: Apana Ale
"""

import pandas as pd

# Step 1: Load both Excel files
df_source = pd.read_excel("bigtable.xlsx", engine='openpyxl')              # file with SDIST(District)
df_target = pd.read_excel("FinalDependentVar.xlsx", engine='openpyxl')     # file to add the column to

# Step 2: Clean column names (optional but recommended)
df_source.columns = df_source.columns.str.strip()
df_target.columns = df_target.columns.str.strip()

# Step 3: Extract only the SDIST(District) column
# Make sure both DataFrames have the same number of rows!
sdist_column = df_source['SDIST(District)']

# Step 4: Add the column to the target DataFrame
df_target['SDIST(District)'] = sdist_column

# Step 5: Save the updated file
df_target.to_excel("FinalDependentVar_Updated.xlsx", index=False)

print("✅ SDIST(District) column added successfully.")
