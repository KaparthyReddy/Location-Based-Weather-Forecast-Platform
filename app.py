import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = '3268ceaa1ab842558f4135205250401'  # Your API key

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather_details')
def weather_details():
    location = request.args.get('location')
    unit = request.args.get('unit', 'metric')  # Default to 'metric' (Celsius)
    
    # Make API call (Ensure you are passing the correct unit)
    url = f'https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}&aqi=no'
    response = requests.get(url)
    weather_data = response.json()

    # Check if the API response is valid
    if 'current' not in weather_data:
        return f"Error: Could not fetch weather data for {location}. Please check the location and try again."

    # Extract temperature correctly (no need for 'temp_' prefix)
    temperature = weather_data['current'].get('temp_' + unit, 'N/A')  # Default to 'N/A' if temp is missing
    
    # Extract weather icon URL
    icon_url = f"http://cdn.weatherapi.com/weather/64x64/{weather_data['current']['condition']['icon']}"

    weather_info = {
        'city': weather_data['location']['name'],
        'country': weather_data['location']['country'],
        'temperature': temperature,
        'description': weather_data['current']['condition']['text'],
        'icon_url': icon_url  # Passing the icon URL to the template
    }

    return render_template('weather_details.html', weather_info=weather_info)

if __name__ == "__main__":
    app.run(debug=True, port=8081)
