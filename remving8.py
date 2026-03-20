# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 22:53:23 2025

@author: Apana Ale
"""

import pandas as pd

# Load your file
file_path = r"clustered_output_1.xlsx"
df = pd.read_excel(file_path)

# Define the relevant variables
m42_columns = ['M42A', 'M42C', 'M42D', 'M42E', 'M42F', 'M42G', 'M42H', 'M42I', 'M42L', 'M42M', 'M42N']
additional_vars = [
    'S418L', 'S418M', 'S418N', 'M45', 'M60', 'S1014AA', 'S1014AB', 'S1014AC',
    'M57A', 'M57B', 'M57E', 'M57F', 'M57G', 'M57H', 'M57I', 'M57J', 'M57K',
    'M57M', 'M57N', 'M57O', 'M57P', 'M57NB', 'M57NC', 'M57ND', 'M57X',
    'M2A', 'M2B', 'M2C', 'M2G', 'M2H', 'M2K', 'M82', 'SDV35BC'
]
all_binary_vars = m42_columns + additional_vars

# Filter only columns that exist in the file
existing_vars = [col for col in all_binary_vars if col in df.columns]

# Apply transformation
df[existing_vars] = df[existing_vars].applymap(lambda x: 1 if x == 1 else 0 if x in [0, 8] else x)

# Save to Excel
df.to_excel(r"checked_file.xlsx", index=False)
