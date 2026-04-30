# ☁️ SkyCast Engine
SkyCast is a streamlined weather intelligence platform that provides hyper-local atmospheric data with a focus on speed, accuracy, and modern aesthetics. It moves beyond basic search by implementing a predictive geolocation engine to ensure users find the exact global coordinates they need.

## 🚀 Key Features
Smart Autocomplete Search: Predictive city, state, and country suggestions to eliminate location ambiguity, such as distinguishing between Delhi, India and Delhi, Canada.

Precision Geolocation: Multi-field input (City, State, Country) for pinpoint meteorological accuracy.

Nexus-Grade UI: A professional dark-mode interface featuring Glassmorphism, backdrop filters, and responsive design.

Dynamic Thermal Analysis: Real-time temperature fetching with support for both Metric and Imperial units.

## 🛠 Tech Stack
Backend: Flask (Python 3.x)

Frontend: Modern CSS3 (Glassmorphism), Vanilla JavaScript (Asynchronous Search)

API: WeatherAPI REST Integration

🏁 Getting Started
Environment Setup:

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask requests
```

Launch the Engine:

```bash
python3 app.py
```

Access the interface at http://localhost:8081.

## 📜 Roadmap

- [x] Smart Location Autocomplete
- [x] Glassmorphic UI Overhaul
- [x] Multi-field Geographic Precision
- [ ] 7-Day Forecast Integration
- [ ] Browser-based GPS Auto-location
