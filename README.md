# Personal Dashboard 🌟

A beautiful, responsive personal dashboard built with Flask that displays weather, news headlines, and inspirational quotes.

![Dashboard Preview](https://img.shields.io/badge/Status-Live-success) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Flask](https://img.shields.io/badge/Flask-2.3-green)

## ✨ Features

- **🌤️ Real-time Weather** - Current weather for Bogotá using Open-Meteo API
- **📰 Latest News** - Top headlines from GNews API with multiple fallbacks
- **💬 Daily Quotes** - Inspirational quotes from Quotable API
- **✅ Task Manager** - Add, complete, and delete personal tasks
- **📱 Responsive Design** - Works on desktop and mobile
- **🔄 Auto-refresh** - Updates every 10 minutes

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **APIs:** Open-Meteo, GNews, Quotable
- **Storage:** Browser Local Storage (tasks)
- **Styling:** CSS Grid & Flexbox

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ffallenangell7/YourPersonalDashboard.git
   cd personal-dashboard

Create virtual environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Configure environment variables

bash
cp .env.txt .env
# Edit .env file with your API keys
Run the application

bash
python app.py
Access dashboard
Navigate to http://127.0.0.1:5000 in your browser

⚙️ Configuration
API Keys
Create a .env file in the root directory:

env
NEWS_API_KEY=your_gnews_api_key_here
Get GNews API Key:

Visit GNews.io

Sign up for a free account

Get your API key from the dashboard

Weather API
Uses Open-Meteo API (no key required)

Default location: Bogotá, Colombia

Coordinates: latitude=4.71, longitude=-74.07

📁 Project Structure
text
personal-dashboard/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables (create this)
├── .gitignore          # Git ignore rules
├── static/
│   ├── css/
│   │   └── style.css    # Main stylesheet
│   └── js/
│       └── script.js    # Frontend JavaScript
└── templates/
    └── index.html       # Main dashboard template
🎯 API Endpoints
GET / - Serve dashboard page

GET /api/weather - Get weather data for Bogotá

GET /api/news - Get top news headlines

GET /api/quote - Get random inspirational quote

🔧 Customization
Change Weather Location
Edit coordinates in app.py:

python
# In get_weather() function
url = 'https://api.open-meteo.com/v1/forecast?latitude=YOUR_LAT&longitude=YOUR_LON&current=temperature_2m,weather_code,relative_humidity_2m,wind_speed_10m'
Add New Widgets
Add HTML in templates/index.html

Create API endpoint in app.py

Add JavaScript function in static/js/script.js

Style in static/css/style.css

🐛 Troubleshooting
Common Issues
API Keys Not Loading:

Ensure .env file exists in root directory

Check variable names match exactly

Restart Flask application after changes

Weather Not Loading:

Open-Meteo API requires no key

Check internet connection

Verify coordinates are valid

News Not Loading:

Verify GNews API key in .env

Check API quota limits

Application will use fallback data

📝 License
This project is licensed under the MIT License.

🤝 Contributing
Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Create a Pull Request
