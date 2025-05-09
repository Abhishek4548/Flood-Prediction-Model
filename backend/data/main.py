from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Path to the uploaded CSV file
CSV_FILE_PATH = r'C:\Users\abhi1\Desktop\Dakshina Kannada\backend\Dakshina Kannada 2019-23C.csv'

# Load the CSV file into a DataFrame at the start
weather_data_df = pd.read_csv(CSV_FILE_PATH)
weather_data_df['datetime'] = pd.to_datetime(weather_data_df['datetime'], dayfirst=True)

def fetch_weather_data_from_csv(city, date):
    """
    Fetch weather data for the given city and date from the CSV file.
    """
    # Ensure the 'name' column matches your city names
    filtered_data = weather_data_df[
        (weather_data_df['name'] == city) &
        (weather_data_df['datetime'] == pd.Timestamp(date))
    ]
    
    if not filtered_data.empty:
        row = filtered_data.iloc[0]  # Get the first row as a Series
        return {
            'temp': row.get('temp', None),
            'humidity': row.get('humidity', None),
            'precip': row.get('precip', None),
            'precipprob': row.get('precipprob', None),
            'windspeed': row.get('windspeed', None),
        }
    else:
        raise ValueError(f"No data found for city {city} on date {date}.")

def get_flood_prediction(precip, humidity, precipprob):
    """
    Determine flood risk based on precipitation, humidity, and precipitation probability.
    """
    if precip < 10 and humidity < 80 and precipprob < 50:
        return "Low flood risk."
    elif (10 <= precip <= 30 and 80 <= humidity <= 90) or (precipprob >= 50):
        return "Moderate risk of flooding. Pay attention to weather."
    elif precip > 30 or humidity > 90 or precipprob > 80:
        return "High risk of flooding. Take protective measures."
    else:
        return "Insufficient data for risk assessment."

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

            # Limit the number of days to 15
            days = min(days, 15)

            predictions = []
            for day in range(days):
                # Calculate the date for each day
                date = (pd.Timestamp.today() + pd.Timedelta(days=day)).strftime('%Y-%m-%d')
                
                # Fetch weather data from the CSV file
                weather_data = fetch_weather_data_from_csv(city, date)
                
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
