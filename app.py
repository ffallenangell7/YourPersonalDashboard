from flask import Flask, render_template, jsonify
import requests
from config import Config
import random

app = Flask(__name__)
app.config.from_object(Config)

# Debug: Check if keys are loading
print("=== CONFIGURATION CHECK ===")
print(f"Weather API Key loaded: {'YES' if Config.WEATHER_API_KEY else 'NO'}")
print(f"News API Key loaded: {'YES' if Config.NEWS_API_KEY else 'NO'}")
print("===========================")

@app.route('/')
def index():
    return render_template('index.html')

# Weather API endpoint using Open-Meteo (NO API KEY REQUIRED) - BOGOTÁ
@app.route('/api/weather')
def get_weather():
    try:
        # Open-Meteo API - no key needed!
        # Bogotá coordinates: latitude=4.71, longitude=-74.07
        url = 'https://api.open-meteo.com/v1/forecast?latitude=4.71&longitude=-74.07&current=temperature_2m,weather_code,relative_humidity_2m,wind_speed_10m'
        print("Calling Open-Meteo API for Bogotá...")
        
        response = requests.get(url)
        print(f"Open-Meteo API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            current = data['current']
            
            # Map weather codes to descriptions and icons
            weather_code = current['weather_code']
            weather_info = get_weather_description(weather_code)
            
            return jsonify({
                'temperature': current['temperature_2m'],
                'description': weather_info['description'],
                'city': 'Bogotá',
                'icon': weather_info['icon'],
                'humidity': current['relative_humidity_2m'],
                'wind_speed': current['wind_speed_10m']
            })
        else:
            print(f"Open-Meteo API error, using fallback")
            return get_weather_fallback()
            
    except Exception as e:
        print(f"Weather API Error: {str(e)}")
        return get_weather_fallback()

def get_weather_description(weather_code):
    """Convert WMO weather codes to descriptions and icons"""
    weather_mapping = {
        # Clear and sunny
        0: {'description': 'Clear sky', 'icon': '☀️'},
        1: {'description': 'Mainly clear', 'icon': '🌤️'},
        2: {'description': 'Partly cloudy', 'icon': '⛅'},
        3: {'description': 'Overcast', 'icon': '☁️'},
        
        # Fog
        45: {'description': 'Fog', 'icon': '🌫️'},
        48: {'description': 'Fog', 'icon': '🌫️'},
        
        # Drizzle
        51: {'description': 'Light drizzle', 'icon': '🌦️'},
        53: {'description': 'Moderate drizzle', 'icon': '🌦️'},
        55: {'description': 'Heavy drizzle', 'icon': '🌦️'},
        
        # Rain
        61: {'description': 'Light rain', 'icon': '🌧️'},
        63: {'description': 'Moderate rain', 'icon': '🌧️'},
        65: {'description': 'Heavy rain', 'icon': '🌧️'},
        
        # Snow
        71: {'description': 'Light snow', 'icon': '❄️'},
        73: {'description': 'Moderate snow', 'icon': '❄️'},
        75: {'description': 'Heavy snow', 'icon': '❄️'},
        
        # Thunderstorm
        95: {'description': 'Thunderstorm', 'icon': '⛈️'},
        96: {'description': 'Thunderstorm with hail', 'icon': '⛈️'},
        99: {'description': 'Heavy thunderstorm', 'icon': '⛈️'}
    }
    
    return weather_mapping.get(weather_code, {'description': 'Unknown', 'icon': '❓'})

def get_weather_fallback():
    """Final fallback with static data for Bogotá"""
    print("Using weather fallback data")
    return jsonify({
        'temperature': 18,
        'description': 'Partly cloudy',
        'city': 'Bogotá',
        'icon': '⛅',
        'humidity': 65,
        'wind_speed': 12
    })

# News API endpoint using GNews
@app.route('/api/news')
def get_news():
    try:
        api_key = Config.NEWS_API_KEY
        
        # Check if we have a GNews API key
        if not api_key or api_key == 'your_gnews_api_key_here':
            print("No GNews API key configured, using fallback news")
            return get_news_fallback()
        
        # GNews API call - get top headlines
        url = f"https://gnews.io/api/v4/top-headlines?token={api_key}&lang=en&max=5"
        print("Calling GNews API...")
        
        response = requests.get(url)
        print(f"GNews API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if we got articles
            if 'articles' in data and data['articles']:
                articles = []
                for article in data['articles'][:5]:  # Get first 5 articles
                    articles.append({
                        'title': article['title'],
                        'url': article['url'],
                        'source': {'name': article['source']['name']},
                        'publishedAt': article['publishedAt']
                    })
                print(f"GNews API Success: {len(articles)} articles loaded")
                return jsonify(articles)
            else:
                print("No articles found in GNews response")
                return get_news_fallback()
        else:
            print(f"GNews API error: {response.status_code}")
            return get_news_fallback()
            
    except Exception as e:
        print(f"GNews API Error: {str(e)}")
        return get_news_fallback()

def get_news_fallback():
    """Fallback news using free APIs"""
    try:
        # Try a free news API as backup
        print("Trying fallback news API...")
        response = requests.get('https://saurav.tech/NewsAPI/top-headlines/category/general/us.json')
        
        if response.status_code == 200:
            data = response.json()
            articles = []
            for article in data['articles'][:5]:
                # Filter out articles with [Removed] title
                if article['title'] != '[Removed]' and article['title']:
                    articles.append({
                        'title': article['title'],
                        'url': article['url'],
                        'source': {'name': article['source']['name']}
                    })
            
            if articles:
                print(f"Fallback news success: {len(articles)} articles loaded")
                return jsonify(articles)
        
        # Final fallback: static news data
        print("Using static news data")
        return get_static_news()
        
    except Exception as e:
        print(f"Fallback news error: {str(e)}")
        return get_static_news()

def get_static_news():
    """Static news data as final fallback"""
    return jsonify([
        {
            'title': 'Tech Industry Continues Rapid Growth in 2025',
            'url': '#',
            'source': {'name': 'Tech News'}
        },
        {
            'title': 'New AI Breakthrough Revolutionizes Healthcare',
            'url': '#', 
            'source': {'name': 'AI Daily'}
        },
        {
            'title': 'Global Push for Sustainable Technology Solutions',
            'url': '#',
            'source': {'name': 'Green Tech'}
        },
        {
            'title': 'Programming Languages Evolution: Trends to Watch',
            'url': '#',
            'source': {'name': 'Dev Weekly'}
        },
        {
            'title': 'Cybersecurity Becomes Top Priority for Businesses',
            'url': '#',
            'source': {'name': 'Security Today'}
        }
    ])

# Quote API endpoint
@app.route('/api/quote')
def get_quote():
    try:
        print("Fetching quote from Quotable API...")
        response = requests.get('https://api.quotable.io/random')
        
        if response.status_code == 200:
            data = response.json()
            print("Quote API Success")
            return jsonify({
                'content': data['content'],
                'author': data['author']
            })
        else:
            print(f"Quote API error: {response.status_code}, using fallback")
            return get_quote_fallback()
            
    except Exception as e:
        print(f"Quote API Error: {str(e)}")
        return get_quote_fallback()

def get_quote_fallback():
    """Fallback quotes"""
    quotes = [
        {
            'content': 'The only way to do great work is to love what you do.',
            'author': 'Steve Jobs'
        },
        {
            'content': 'Innovation distinguishes between a leader and a follower.',
            'author': 'Steve Jobs'
        },
        {
            'content': 'The future belongs to those who believe in the beauty of their dreams.',
            'author': 'Eleanor Roosevelt'
        },
        {
            'content': 'Success is not final, failure is not fatal: it is the courage to continue that counts.',
            'author': 'Winston Churchill'
        },
        {
            'content': 'The way to get started is to quit talking and begin doing.',
            'author': 'Walt Disney'
        }
    ]
    print("Using fallback quote")
    return jsonify(random.choice(quotes))

if __name__ == '__main__':
    print("\n🚀 Starting Personal Dashboard...")
    print("📍 Weather: Bogotá (Open-Meteo API)")
    print("📰 News: GNews API with fallbacks")
    print("💬 Quotes: Quotable API")
    print("📊 Access your dashboard at: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True)