from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pandas as pd
import joblib
import requests
import numpy as np

def train_flood_model():
    print("Starting Model Training")
    historical_data = pd.read_csv(r"C:\Users\abhi1\Desktop\Dakshina Kannada\backend\data\Dmerged_flood_data.csv")
    valid_data = historical_data.dropna()
    X = valid_data[['temp', 'humidity', 'precipprob', 'windspeed']]
    y = valid_data['precip']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Calculate evaluation metrics
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Absolute Error (MAE): {mae}")
    print(f"Mean Squared Error (MSE): {mse}")
    print(f"Root Mean Squared Error (RMSE): {rmse}")
    print(f"R-Squared (R2): {r2}")

    joblib.dump(model, r'C:\Users\abhi1\Desktop\Dakshina Kannada\backend\model\flood_prediction_modelD.pkl')
    print("Flood Prediction Model saved as 'flood_prediction_modelD.pkl'.")

train_flood_model()
