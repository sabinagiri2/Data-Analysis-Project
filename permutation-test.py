# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 14:46:08 2025
@author: Apana Ale
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt

# Step 1: Load the dataset
df = pd.read_excel("checked_file.xlsx")  # Replace with your file path

# Step 2: Define features and target variable
features = ['V001', 'V106', 'V190', 'SDIST', 'V701', 'V131',
            'V704', 'V024', 'SECOREG', 'V025', 'V130']
target = 'Cluster'

# Step 3: Drop rows with missing values
df_clean = df[features + [target]].dropna()

# Step 4: Convert all features to categorical type
df_clean[features] = df_clean[features].astype('category')

# Step 5: Define X and y
X = df_clean[features]
y = df_clean[target]

# Step 6: Encode target variable
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Step 7: Define and train the XGBoost classifier on full data
model = XGBClassifier(
    max_depth=7,
    use_label_encoder=False,
    eval_metric='mlogloss',
    enable_categorical=True
)
model.fit(X, y_encoded)

# Step 8: Perform permutation feature importance on full data
result = permutation_importance(
    model, X, y_encoded,
    n_repeats=30,
    random_state=42,
    n_jobs=-1
)

# Step 9: Descriptive feature names mapping
feature_names_map = {
    'V001': 'Cluster Number',
    'V106': 'Highest Education Level',
    'V190': 'Wealth Index',
    'SDIST': 'District',
    'V701': 'Husband\'s Education',
    'V131': 'Ethnicity',
    'V704': 'Husband\'s Occupation',
    'V024': 'Province',
    'SECOREG': 'Ecological Region',
    'V025': 'Type of Residence',
    'V130': 'Religion'
}

# Step 10: Create a dataframe of results
importance_df = pd.DataFrame({
    'Feature': X.columns,
    'Importance Mean': result.importances_mean,
    'Importance Std': result.importances_std
})
importance_df['Feature (Label)'] = importance_df['Feature'].map(feature_names_map)

# Step 11: Sort features from high to low importance
importance_df = importance_df.sort_values(by='Importance Mean', ascending=False)

# Step 12: Print the feature importances
print("\nPermutation Feature Importance:")
print(importance_df[['Feature (Label)', 'Importance Mean', 'Importance Std']])

# Step 13: Plot without error bars, sorted from high to low
plt.figure(figsize=(12, 6))
plt.bar(importance_df['Feature (Label)'], importance_df['Importance Mean'])  # no error bars
plt.xticks(rotation=45, ha='right')
plt.ylabel("Mean Decrease in Accuracy")
plt.xlabel("Independent Variables (sorted)")
plt.title("Permutation Feature Importance (XGBoost on Full Data)\n(High to Low Importance)")
plt.tight_layout()
plt.show()
