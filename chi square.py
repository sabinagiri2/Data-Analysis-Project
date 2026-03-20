import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

# Load Excel file with crosstabs
file_path = "crosstab_tables.xlsx"  # Change path if needed
xls = pd.ExcelFile(file_path)
sheet_names = xls.sheet_names

# Function to compute Cramér's V (strength of association)
def cramers_v(confusion_matrix):
    chi2, _, _, _ = chi2_contingency(confusion_matrix)
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    # Correct for bias in large tables
    phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1)) 
    rcorr = r - ((r-1)**2)/(n-1)
    kcorr = k - ((k-1)**2)/(n-1)
    return np.sqrt(phi2corr / min((kcorr-1), (rcorr-1)))

# Store results
results = []

# Process each sheet
for sheet in sheet_names:
    df = xls.parse(sheet)
    df_clean = df.select_dtypes(include='number')
    
    if df_clean.empty or df_clean.shape[0] < 2 or df_clean.shape[1] < 2:
        continue  # skip sheets with insufficient data
    
    chi2, p, dof, expected = chi2_contingency(df_clean)
    v = cramers_v(df_clean)
    relationship_percent = round(v * 100, 2)  # scale to percentage
    
    results.append({
        "Variable": sheet,
        "p-value": round(p, 4),
        "Relationship (%)": relationship_percent
    })

# Create and sort result table
results_df = pd.DataFrame(results)
results_df.sort_values(by="Relationship (%)", ascending=False, inplace=True)
results_df.reset_index(drop=True, inplace=True)

# Show the table
print(results_df)

# Optionally, save to Excel
results_df.to_excel("cluster_variable_relationships.xlsx", index=False)
