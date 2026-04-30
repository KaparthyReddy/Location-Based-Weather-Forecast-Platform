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
    if len(query) < 2: return jsonify([])
    url = f'https://api.weatherapi.com/v1/search.json?key={API_KEY}&q={query}'
    return jsonify(requests.get(url).json())

@app.route('/weather_details')
def weather_details():
    city = request.args.get('city', '').strip()
    state = request.args.get('state', '').strip()
    country = request.args.get('country', '').strip()
    unit = request.args.get('unit', 'metric')
    
    # Combined search query
    full_query = f"{city} {state} {country}".strip()
    url = f'https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={full_query}&days=7'
    data = requests.get(url).json()

    if 'current' not in data: return "Location not found.", 404

    # Integrate the Legacy logic: Kelvin Conversion
    temp_c = data['current']['temp_c']
    if unit == 'kelvin':
        display_temp = round(temp_c + 273.15, 2)
        label = "K"
    elif unit == 'imperial':
        display_temp = data['current']['temp_f']
        label = "°F"
    else:
        display_temp = temp_c
        label = "°C"
    
    weather_info = {
        'city': data['location']['name'],
        'region': data['location']['region'],
        'country': data['location']['country'],
        'temperature': display_temp,
        'unit_label': label,
        'description': data['current']['condition']['text'],
        'icon_url': "https:" + data['current']['condition']['icon'],
        'forecast': []
    }

    # Apply conversion to the 7-day forecast too
    for day in data['forecast']['forecastday']:
        avg_c = day['day']['avgtemp_c']
        if unit == 'kelvin': f_temp = round(avg_c + 273.15, 1)
        elif unit == 'imperial': f_temp = day['day']['avgtemp_f']
        else: f_temp = avg_c

        weather_info['forecast'].append({
            'date': day['date'],
            'avg_temp': f_temp,
            'icon': "https:" + day['day']['condition']['icon']
        })

    return render_template('weather_details.html', weather_info=weather_info)

if __name__ == "__main__":
    app.run(debug=True, port=8081)
