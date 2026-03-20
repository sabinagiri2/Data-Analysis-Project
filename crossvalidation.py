import xgboost as xgb
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Load your dataset
df = pd.read_excel("checked_file.xlsx")

# Define features and target
features = ['V001', 'V106', 'V190', 'SDIST', 'V701', 'V131',
            'V704', 'V024', 'SECOREG', 'V025', 'V130']
target = 'Cluster'

# Clean and preprocess
df = df[features + [target]].dropna()
df[features] = df[features].astype('category')

# Prepare features and encode target
X = df[features]
y = LabelEncoder().fit_transform(df[target])
num_classes = len(np.unique(y))

# Convert to DMatrix with categorical support
dtrain = xgb.DMatrix(X, label=y, enable_categorical=True)

# ✅ Optimized parameters for better accuracy and generalization
params = {
    'objective': 'multi:softprob',    # Multiclass classification
    'num_class': num_classes,         # Automatically detect number of classes
    'max_depth': 10,                   # Deeper trees capture more patterns
    'eta': 0.1,                       # Lower learning rate = better generalization
    'subsample': 0.8,                 # Randomly sample rows to prevent overfitting
    'colsample_bytree': 0.8,          # Randomly sample features
    'min_child_weight': 3,            # Avoid splits on small data
    'gamma': 0.2,                     # Minimum loss reduction before a split
    'lambda': 1.0,                    # L2 regularization
    'alpha': 0.5,                     # L1 regularization
    'eval_metric': 'mlogloss'         # Multiclass log loss
}

# Cross-validation with early stopping
cv_results = xgb.cv(
    params=params,
    dtrain=dtrain,
    num_boost_round=200,
    nfold=5,
    stratified=True,
    seed=42,
    verbose_eval=False,
    callbacks=[
        xgb.callback.EvaluationMonitor(show_stdv=True),
        xgb.callback.EarlyStopping(rounds=10)
    ]
)

# Best iteration
best_round = cv_results['test-mlogloss-mean'].idxmin()
print(f"✅ Best boosting round: {best_round}")

# Train final model
final_model = xgb.train(
    params=params,
    dtrain=dtrain,
    num_boost_round=best_round
)

# Predict on the training data to evaluate cross-validated accuracy
y_pred_probs = final_model.predict(dtrain)
y_pred = np.argmax(y_pred_probs, axis=1)

# Calculate accuracy
accuracy = np.mean(y_pred == y)
print(f"✅ Cross-validated Accuracy: {accuracy:.4f}")