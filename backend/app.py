from flask import Flask, request, jsonify
import pandas as pd
import joblib
import requests
from flask_cors import CORS
from model import add_new_data_to_training_set, train_flood_model  # Import additional model functions

app = Flask(__name__)
CORS(app)

# Load the prediction model
model_path = r'C:\Users\abhi1\Desktop\Dakshina Kannada\backend\model\flood_model.pkl'
model = joblib.load(model_path)

# API configuration
API_KEY = 'CG89EXBBQTD2UDD32R8X2GXK5'  # Replace with your actual API key
BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'

def fetch_weather_data_from_api(city, date):
    """
    Fetch weather data for the given city and date from the Visual Crossing API.
    """
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
            raise ValueError(f"Data for city{city} on date{date} is not available.")
    else:
        raise ValueError(f"Error Retriving data: {response.status_code}, {response.text}")

def get_flood_prediction(precip, humidity, precipprob):
    """
    Determine flood risk based on precipitation, humidity, and precipitation probability.
    """
    if precip < 10 and humidity < 80 and precipprob < 50:
        return "Low flood risk."
    elif (10 <= precip <= 30 and 80 <= humidity <= 90) or (precipprob >= 50):
        return "Moderate risk of flooding. Pay attention to weather"
    elif precip > 30 or humidity > 90 or precipprob > 80:
        return "High risk of flooding. Take Protective measures."
    else:
        return "Insufficent data for risk assessment."

@app.route('/predict_flood', methods=['GET', 'POST'])
def predict_flood():
    """
    Predict flood risk based on weather data for a city over the next specified number of days.
    """
    if request.method == 'GET':
        return jsonify({"message": "This is a flood prediction API."}), 200
    else:
        try:
            data = request.get_json()
            print(f"Received data: {data}")

            city = data.get('city')
            days = int(data.get('days'))

            # Limit the number of days to 10
            days = min(days, 25)

            predictions = []
            for day in range(days):
                # Fetch weather data for each day
                weather_data = fetch_weather_data_from_api(city, (pd.Timestamp.today() + pd.Timedelta(days=day)).strftime('%Y-%m-%d'))
                
                precip = weather_data['precip']
                humidity = weather_data['humidity']
                precipprob = weather_data['precipprob']
                
                # Get flood risk prediction
                flood_risk_prediction = get_flood_prediction(precip, humidity, precipprob)

                predictions.append({
                    'day': int(day + 1),
                    'predicted_flood_risk': flood_risk_prediction,
                    'precip': precip,
                    'humidity': humidity,
                    'precipprob': precipprob,
                })

            print(f"Predictions: {predictions}")
            return jsonify(predictions), 200

        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    """
    Default route for the API.
    """
    return "Welcome to the Flood Risk Prediction API!"

if __name__ == "__main__":
    app.run(debug=True)
