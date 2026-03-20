import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Load your dataset
df = pd.read_excel("clustered_output.xlsx")

# Define independent variables and target
X = df[['V106']]
y = df['Cluster']

# Drop missing values
X = X.dropna()
y = y.loc[X.index]

# Encode categorical variables with one-hot encoding
X_encoded = pd.get_dummies(X, drop_first=True)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Initialize Decision Tree with entropy and max_depth=3
clf = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=0)
clf.fit(X_train, y_train)

# Plot the decision tree
plt.figure(figsize=(20, 10))
plot_tree(
    clf,
    feature_names=X_encoded.columns,
    class_names=[str(label) for label in sorted(y.unique())],
    filled=True,
    rounded=True,
    fontsize=8
)
plt.title("Decision Tree (max_depth=3, criterion=entropy)")
plt.show()

# Print depth and accuracy
print(f"🌲 Tree Depth: {clf.get_depth()}")
print(f"✅ Test Accuracy: {clf.score(X_test, y_test):.4f}")
