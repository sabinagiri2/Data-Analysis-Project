# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 14:02:57 2025

@author: Apana Ale
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from xgboost import XGBClassifier
from scipy.stats import randint, uniform
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_excel("checked_file.xlsx")

# Define features and target
features = ['V001', 'V106', 'V190', 'SDIST', 'V701', 'V131',
            'V704', 'V024', 'SECOREG', 'V025', 'V130']
target = 'Cluster'

# Drop missing values and convert features to categorical
df_clean = df[features + [target]].dropna()
df_clean[features] = df_clean[features].astype('category')

# Prepare features and label
X = df_clean[features]
y_raw = df_clean[target]
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y_raw)
label_names = label_encoder.classes_.astype(str)

# Define XGBoost classifier
xgb_model = XGBClassifier(
    objective='multi:softprob',
    num_class=len(label_names),
    use_label_encoder=False,
    eval_metric='mlogloss',
    enable_categorical=True
)

# Define hyperparameter distributions
param_dist = {
    'max_depth': randint(3, 10),
    'learning_rate': uniform(0.01, 0.3),         # 0.01 to 0.31
    'n_estimators': randint(100, 500),           # number of trees
    'subsample': uniform(0.6, 0.4),              # 0.6 to 1.0
    'colsample_bytree': uniform(0.6, 0.4),       # 0.6 to 1.0
    'min_child_weight': randint(1, 8),
    'gamma': uniform(0.0, 0.3),
    'reg_alpha': uniform(0.0, 0.5),
    'reg_lambda': uniform(0.5, 1.5)
}

# Define cross-validation
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# RandomizedSearchCV setup
random_search = RandomizedSearchCV(
    estimator=xgb_model,
    param_distributions=param_dist,
    n_iter=30,  # You can increase to 50 or 100 for more thorough search
    scoring='accuracy',
    cv=cv,
    verbose=1,
    n_jobs=-1,
    random_state=42
)

# Fit RandomizedSearchCV
random_search.fit(X, y)

# Get the best model and parameters
best_model = random_search.best_estimator_
print("\n✅ Best Parameters Found:")
print(random_search.best_params_)

# Predict class probabilities and get final predictions
y_pred_proba = best_model.predict(X)
y_pred = np.argmax(y_pred_proba, axis=1)

# Accuracy
accuracy = accuracy_score(y, y_pred)
print(f"\n✅ Accuracy on Entire Dataset: {accuracy:.4f}")

# Classification report
print("\n📊 Classification Report:")
print(classification_report(y, y_pred, target_names=label_names))

# Confusion Matrix
cm = confusion_matrix(y, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=label_names)
disp.plot(cmap='Blues')
plt.title("Confusion Matrix")
plt.show()
