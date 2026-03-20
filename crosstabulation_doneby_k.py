import pandas as pd

# Load the dataset
file_path = "C:/Users/ADMIN/OneDrive/Desktop/finalproject/finaltable.xlsx"
df = pd.read_excel(file_path)

# Define X and Y variables
x_vars = ['V106', 'V024', 'V025', 'V130', 'V131', 'V190',
          'V701', 'V704', 'SECOREG', 'SDIST', 'V001']
y_var = 'Cluster'

# Create percentage-wise cross-tabulations
percentage_tables = {}
for var in x_vars:
    if var in df.columns and y_var in df.columns:
        # Normalize across columns (i.e., within each cluster)
        crosstab = pd.crosstab(df[var], df[y_var], normalize='columns') * 100
        percentage_tables[var] = crosstab.round(2)

# Save all percentage crosstabs to an Excel file
output_path = "C:/Users/ADMIN/OneDrive/Desktop/finalproject/crosstab_percentage_tables.xlsx"
with pd.ExcelWriter(output_path) as writer:
    for var, table in percentage_tables.items():
        table.to_excel(writer, sheet_name=var[:31])  # Excel sheet name limit is 31 characters

print("Percentage-wise cross-tabulation saved to:", output_path)
