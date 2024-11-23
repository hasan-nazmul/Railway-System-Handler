import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse import csr_matrix
import numpy as np
import pickle

# Load the dataset
dataset = pd.read_csv('RailData.csv')

# Prepare the data
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

# Encode categorical variables
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0,1])], remainder='passthrough')

X = ct.fit_transform(X).toarray()

# Save Encoder
with open('column_transformer.pkl', 'wb') as file: 
    pickle.dump(ct, file)
    print("column transformer saved successfully!")

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the models
# models = {
#     'Linear Regression': LinearRegression(),
#     'Decision Tree': DecisionTreeRegressor(random_state=42),
#     'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
#     'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
# }

# Evaluate the models
# for name, model in models.items():
#     model.fit(X_train, y_train)
#     y_pred = model.predict(X_test)
#     r2 = r2_score(y_test, y_pred)
#     print(f'{name} R² score: {r2:.4f}')

regressor = GradientBoostingRegressor(n_estimators=100, random_state=42)
regressor.fit(X_train, y_train)

# Save the model to a file using pickle 
with open('regression_model.pkl', 'wb') as file: 
    pickle.dump(regressor, file)
    print("Model saved successfully!")

# Load the model from the file
with open('regression_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

# Make predictions using the loaded model
y_pred = loaded_model.predict(X_test)

# Evaluate the loaded model
r2 = r2_score(y_test, y_pred)
print(f'R² score of the loaded model: {r2:.4f}')