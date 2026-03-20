import pandas as pd

# Load the Excel file
file_path = 'cleaned_weights.xlsx'  # Replace with your file path
sheet_name = 'Sheet1'         # Change if needed
column_name = 'SDIST(District)'  # Exact column name based on your Excel

# Read the Excel file
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Count how many times each province (1–7) appears
district_counts = df[column_name].value_counts().sort_index()

# Calculate the ratio (as a fraction and percent)
total = district_counts.sum()
district_ratios = district_counts / total

# Create result DataFrame
result = pd.DataFrame({
    'District': district_counts.index,
    'Count': district_counts.values,
    'Ratio': district_ratios.values,
    'Ratio (%)': (district_ratios.values * 100).round(2)
})

# Save result to a new Excel file
result.to_excel('district_ratios.xlsx', index=False)

print(result)
