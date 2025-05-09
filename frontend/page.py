import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime, timedelta
import requests
import pandas as pd

# Your existing function to fetch weather data
def predict_weather_data(city, start_date, end_date):
    API_KEY = 'CG89EXBBQTD2UDD32R8X2GXK5'
    BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'

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

    if response.status_code != 200:
        raise ValueError(f"Error fetching data: {response.status_code}, {response.text}")

    try:
        data = response.json()
    except ValueError:
        raise ValueError("Failed to parse JSON. Response content: " + response.text)

    if 'days' in data:
        df = pd.DataFrame(data['days'])
        df['city'] = city
        return df
    else:
        raise ValueError("No data available for the requested period.")

def predict_flood(city, start_date, end_date):
    df = predict_weather_data(city, start_date, end_date)
    # Simple flood prediction based on precipitation
    flood_df = df[df['precip'] > 50]
    if not flood_df.empty:
        return "Flood predicted"
    else:
        return "No flood predicted"

class WeatherPredictor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Weather Predictor")

        # Create input fields
        self.city_label = tk.Label(self.window, text="City:")
        self.city_label.grid(row=0, column=0, padx=5, pady=5)
        self.city_entry = tk.Entry(self.window, width=30)
        self.city_entry.grid(row=0, column=1, padx=5, pady=5)

        self.start_date_label = tk.Label(self.window, text="Start Date (YYYY-MM-DD):")
        self.start_date_label.grid(row=1, column=0, padx=5, pady=5)
        self.start_date_entry = tk.Entry(self.window, width=30)
        self.start_date_entry.grid(row=1, column=1, padx=5, pady=5)

        self.end_date_label = tk.Label(self.window, text="End Date (YYYY-MM-DD):")
        self.end_date_label.grid(row=2, column=0, padx=5, pady=5)
        self.end_date_entry = tk.Entry(self.window, width=30)
        self.end_date_entry.grid(row=2, column=1, padx=5, pady=5)

        # Create button to predict weather
        self.predict_button = tk.Button(self.window, text="Predict Weather", command=self.predict_weather)
        self.predict_button.grid(row=3, column=0, padx=5, pady=5)

        # Create button to predict flood
        self.flood_button = tk.Button(self.window, text="Predict Flood", command=self.predict_flood)
        self.flood_button.grid(row=3, column=1, padx=5, pady=5)

        # Create text box to display result
        self.result_text = tk.Text(self.window, width=50, height=10)
        self.result_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def predict_weather(self):
        city = self.city_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        try:
            df = predict_weather_data(city, start_date, end_date)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, df.to_string())
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def predict_flood(self):
        city = self.city_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        try:
            result = predict_flood(city, start_date, end_date)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = WeatherPredictor()
    app.run()
