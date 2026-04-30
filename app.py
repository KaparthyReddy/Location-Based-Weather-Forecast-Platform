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
    # WeatherAPI search endpoint also supports lat,long strings
    url = f'https://api.weatherapi.com/v1/search.json?key={API_KEY}&q={query}'
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/weather_details')
def weather_details():
    city = request.args.get('city', '').strip()
    state = request.args.get('state', '').strip()
    country = request.args.get('country', '').strip()
    unit = request.args.get('unit', 'metric')
    
    full_query = f"{city} {state} {country}".strip()
    # Changed to forecast.json and requested 7 days
    url = f'https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={full_query}&days=7&aqi=no'
    response = requests.get(url)
    data = response.json()

    if 'current' not in data:
        return "Error: Location not found.", 404

    u_key = 'c' if unit == 'metric' else 'f'
    
    weather_info = {
        'city': data['location']['name'],
        'region': data['location']['region'],
        'country': data['location']['country'],
        'temperature': data['current'].get(f'temp_{u_key}'),
        'unit_label': '°C' if unit == 'metric' else '°F',
        'description': data['current']['condition']['text'],
        'icon_url': "https:" + data['current']['condition']['icon'],
        'forecast': []
    }

    for day in data['forecast']['forecastday']:
        weather_info['forecast'].append({
            'date': day['date'],
            'avg_temp': day['day'].get(f'avgtemp_{u_key}'),
            'icon': "https:" + day['day']['condition']['icon']
        })

    return render_template('weather_details.html', weather_info=weather_info)

if __name__ == "__main__":
    app.run(debug=True, port=8081)
