from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import joblib
import requests


def train_flood_model():
    print("Starting Model Training") 
    historical_data = pd.read_csv(r"C:\Users\abhi1\Desktop\Dakshina Kannada\backend\data\Dmerged_flood_data.csv")
    
    valid_data = historical_data.dropna()
    
    X = valid_data[['temp', 'humidity', 'precip', 'precipprob', 'windspeed']]
    y = valid_data['precip']
    
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X, y)
    
    
    joblib.dump(model, r'C:\Users\abhi1\Desktop\Dakshina Kannada\backend\model\flood_prediction_modelD.pkl')
    print("Flood Prediction Model saved as 'flood_prediction_modelD.pkl'.")

def fetch_weather_data_from_api(city, date):
    """
    Gets weather data for a specific city and date.
    """
    BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Dakshina%20Kannada?unitGroup=us&key=CG89EXBBQTD2UDD32R8X2GXK5&contentType=json'
    API_KEY = 'CG89EXBBQTD2UDD32R8X2GXK5'
    url = f"{BASE_URL}/{city}/{date}"
    params = {
        'unitGroup': 'metric',
        'key': API_KEY,
        'include': 'days',
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'days' in data and len(data['days']) > 0:
            day_data = data['days'][0]
            return {
                'temp': day_data.get('temp', None),
                'humidity': day_data.get('humidity', None),
                'precip': day_data.get('precip', None),
                'precipprob': day_data.get('precipprob', None),
                'windspeed': day_data.get('windspeed', None),
            }
        else:
            raise ValueError(f"Meteorological data is not available for{city}on{date}.")
    else:
        raise ValueError(f"Error retrieving data: {response.status_code}, {response.text}")

def add_new_data_to_training_set(city, day, predicted_flood_risk, actual_flood_risk):
    """
    Adds new data to the training set if the difference between the prediction and the actual data is Significant.
    """
    full_data = pd.read_csv(r'C:\Users\abhi1\Desktop\Dakshina Kannada\backend\data\Dmerged_flood_data.csv')
    
    date = pd.Timestamp.today() + pd.Timedelta(days=day)
    formatted_date = date.strftime('%Y-%m-%d')

    weather_data = fetch_weather_data_from_api(city, formatted_date)
    
    new_data = {
        'datetime': formatted_date,
        'temp': weather_data['temp'],
        'humidity': weather_data['humidity'],
        'precip': weather_data['precip'],
        'precipprob': weather_data['precipprob'],
        'windspeed': weather_data['windspeed'],
        'city': city,
    }
    
    new_data_df = pd.DataFrame([new_data])
    full_data = pd.concat([full_data, new_data_df], ignore_index=True)
    
    full_data.to_csv(r'C:\Users\abhi1\Desktop\Dakshina Kannada\backend\data\Dmerged_flood_data.csv', index=False)
    print(f"Added data for city{city} on {formatted_date}.")
