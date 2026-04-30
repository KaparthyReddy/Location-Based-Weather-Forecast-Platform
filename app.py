import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
API_KEY = '3268ceaa1ab842558f4135205250401'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search_suggest')
def search_suggest():
    query = request.args.get('q', '')
    if len(query) < 2:
        return jsonify([])
    url = f'https://api.weatherapi.com/v1/search.json?key={API_KEY}&q={query}'
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/weather_details')
def weather_details():
    city = request.args.get('city', '').strip()
    state = request.args.get('state', '').strip()
    country = request.args.get('country', '').strip()
    unit = request.args.get('unit', 'metric')
    
    # Building a more precise query for the final fetch
    full_query = f"{city} {state} {country}".strip()

    url = f'https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={full_query}&aqi=no'
    response = requests.get(url)
    weather_data = response.json()

    if 'current' not in weather_data:
        return f"Error: Location not found.", 404

    unit_key = 'c' if unit == 'metric' else 'f'
    temperature = weather_data['current'].get(f'temp_{unit_key}', 'N/A')
    icon_url = "https:" + weather_data['current']['condition']['icon']

    weather_info = {
        'city': weather_data['location']['name'],
        'region': weather_data['location']['region'],
        'country': weather_data['location']['country'],
        'temperature': temperature,
        'unit_label': '°C' if unit == 'metric' else '°F',
        'description': weather_data['current']['condition']['text'],
        'icon_url': icon_url
    }
    return render_template('weather_details.html', weather_info=weather_info)

if __name__ == "__main__":
    app.run(debug=True, port=8081)
