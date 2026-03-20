import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import xgboost as xgb
from xgboost import plot_tree
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load the dataset
df = pd.read_excel("finaltable.xlsx")  # 🔁 Update with correct file path if needed

# Step 2: Select features and drop rows with missing values
features = df[['V106', 'V190', 'V701', 'SDIST']].dropna()
target = df['Cluster'].loc[features.index]

# Step 3: Recode Cluster values from [1, 2] to [0, 1]
target = target.map({1: 0, 2: 1})

# Step 4: One-hot encode categorical features
features_encoded = pd.get_dummies(features.astype('category'))

# Step 5: Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(features_encoded)

# Step 6: Apply SMOTE for balancing classes
smote = SMOTE(random_state=42)
X_balanced, y_balanced = smote.fit_resample(X_scaled, target)

# Step 7: Print number of samples per class after SMOTE
cluster_counts = pd.Series(y_balanced).value_counts()
print("Number of samples after SMOTE:")
print(f"Cluster 0 (original label 1): {cluster_counts[0]}")
print(f"Cluster 1 (original label 2): {cluster_counts[1]}")

# Step 8: Train the XGBoost model
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
model.fit(X_balanced, y_balanced)

# Step 9: Predict on original (unbalanced) data
y_pred = model.predict(X_scaled)

# Step 10: Evaluation metrics
cm = confusion_matrix(target, y_pred)
print("\nConfusion Matrix:\n", cm)
print("\nClassification Report:\n", classification_report(target, y_pred))

# Step 11: Plot confusion matrix
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=[0, 1], yticklabels=[0, 1])
plt.xlabel('Predicted Label')
plt.ylabel('Actual Label')
plt.title('Confusion Matrix')
plt.tight_layout()
plt.show()

# Step 12: Plot the first decision tree without Graphviz
plt.figure(figsize=(25, 15))
plot_tree(model, num_trees=0, rankdir='LR')  # rankdir='LR' = left to right tree layout
plt.title("XGBoost - First Decision Tree")
plt.show()
