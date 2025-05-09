from datetime import datetime
import requests
import pandas as pd
import os

API_KEY = 'CG89EXBBQTD2UDD32R8X2GXK5'
BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'

def fetch_weather_data(city, start_date, end_date):
    """
    Fetch weather data from Visual Crossing API.
    :param city: Name of the city (e.g., "Dakshina_Kannada").
    :param start_date: Start date in format YYYY-MM-DD.
    :param end_date: End date in format YYYY-MM-DD.
    :return: Pandas DataFrame with weather data.
    """
    # Validate date order
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    if start > end:
        raise ValueError(f"Start date ({start_date}) cannot be later than end date ({end_date}).")

    url = f"{BASE_URL}/{city}/{start_date}/{end_date}"
    params = {
        'unitGroup': 'metric',
        'key': API_KEY,
        'include': 'days'
    }
    response = requests.get(url, params=params)

    # Debugging: Check response status and content
    if response.status_code != 200:
        raise ValueError(f"Error fetching data: {response.status_code}, {response.text}")
    try:
        data = response.json()
    except ValueError:
        raise ValueError("Failed to parse JSON. Response content: " + response.text)

    if 'days' in data:
        return pd.DataFrame(data['days'])
    else:
        raise ValueError("No data available for the requested period.")

def save_weather_data_to_csv(city, start_date, end_date, file_name):
    """
    Fetch weather data and save it to a CSV file.
    :param city: Name of the city.
    :param start_date: Start date in format YYYY-MM-DD.
    :param end_date: End date in format YYYY-MM-DD.
    :param file_name: File name for the CSV.
    """
    df = fetch_weather_data(city, start_date, end_date)
    df['city'] = city
    # Ensure the directory exists
    directory = os.path.dirname(file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    df.to_csv(file_name, index=False)
    print(f"Data for {city} saved to file {file_name}")

if __name__ == "__main__":
    cities = ["Dakshina_Kannada"]
    start_date = "2021-06-01"
    end_date = "2023-12-31"
    for city in cities:
        try:
            save_weather_data_to_csv(city, start_date, end_date, f"data/{city.lower()}_weather.csv")
        except ValueError as e:
            print(f"Error for city {city}: {e}")
