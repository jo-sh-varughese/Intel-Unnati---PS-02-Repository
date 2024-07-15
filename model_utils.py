import pandas as pd # type: ignore
from sklearn.ensemble import RandomForestRegressor # type: ignore
from sklearn.preprocessing import StandardScaler # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
import joblib # type: ignore
import numpy as np # type: ignore
import seaborn as sns # type: ignore
import matplotlib.pyplot as plt # type: ignore
import tensorflow as tf # type: ignore
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense # type: ignore

# Load data
data = pd.read_csv('health_data.csv')

# Basic feature engineering
data['BMI'] = data['weight'] / (data['height']/100)**2

# Define features and target variables
X = data[['age', 'weight', 'height', 'steps_per_day', 'heart_rate', 'sleep_hours', 'calories_intake', 'cholesterol_level', 'BMI']]
y = data['health_score']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train a RandomForest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)

# Save the model and scaler
joblib.dump(rf_model, 'health_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

# Create a deep learning model
def create_deep_learning_model():
    model = Sequential()
    model.add(Dense(128, input_dim=X_train_scaled.shape[1], activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

# Train the deep learning model
dl_model = create_deep_learning_model()
dl_model.fit(X_train_scaled, y_train, epochs=50, batch_size=32, validation_split=0.2, verbose=1)

# Save the deep learning model
dl_model.save('health_dl_model.h5')

# Visualization function
def visualize_health_data(data):
    plt.figure(figsize=(12, 8))
    sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
    plt.title('Health Data Correlation Heatmap')
    plt.show()

# Function to predict health score
def predict_health(input_data):
    model = joblib.load('health_model.pkl')
    scaler = joblib.load('scaler.pkl')
    input_df = pd.DataFrame([input_data])
    input_df['BMI'] = input_df['weight'] / (input_df['height']/100)**2
    input_scaled = scaler.transform(input_df)
    health_score = model.predict(input_scaled)[0]
    return health_score

# Function to generate advice based on health score
def generate_advice(health_score):
    if health_score < 40:
        return "Your health is in critical condition. Please consult a doctor immediately."
    elif health_score < 60:
        return "Your health needs improvement. Regular exercise and a balanced diet are recommended."
    elif health_score < 80:
        return "You are doing okay, but there's room for improvement. Keep up the good habits!"
    else:
        return "Great job! Keep maintaining your healthy lifestyle."
