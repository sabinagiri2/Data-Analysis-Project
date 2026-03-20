import pandas as pd

# Load your dataset
df = pd.read_excel('cleaned_bigtable2.xlsx')

# Use short variable names exactly as in your Excel
columns_to_check = [
    'M42A', 'M42C', 'M42D', 'M42E', 'M42F', 'M42G', 'M42H', 'M42I', 'M42L', 'M42M', 'M42N',
    'S418L', 'S418M', 'S418N', 'M14', 'M1', 'M1A', 'M1D', 'M45', 'M46', 'M60',
    'S1014AA', 'S1014AB', 'S1014AC', 'M57A', 'M57B', 'M57E', 'M57F', 'M57G', 'M57H', 'M57I',
    'M57J', 'M57K', 'M57M', 'M57N', 'M57O', 'M57P', 'M57NB', 'M57NC', 'M57ND', 'M57X',
    'M2A', 'M2B', 'M2C', 'M2G', 'M2H', 'M2K', 'MH17A', 'MH17B', 'MH17C', 'M82'
]

# Ensure columns are numeric (important for comparison)
df[columns_to_check] = df[columns_to_check].apply(pd.to_numeric, errors='coerce')

# Remove rows where ALL of the specified columns are zero or NaN
df_cleaned = df[~(df[columns_to_check].fillna(0) == 0).all(axis=1)]

# Save to a new Excel file
df_cleaned.to_excel('cleaned_bigtable2.xlsx', index=False)

print("✅ Cleaned data saved as 'cleaned_bigtable.xlsx'.")
