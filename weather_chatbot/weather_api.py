import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str) -> dict:
    """
    Fetch current weather data for a given city.
    
    Args:
        city: Name of the city
        
    Returns:
        Dictionary containing weather information
    """
    try:
        params = {
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric"  # Use Celsius
        }
        
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract relevant information
        weather_info = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }
        
        return weather_info
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"error": f"City '{city}' not found. Please check the city name."}
        else:
            return {"error": f"API error: {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to fetch weather data: {str(e)}"}


def format_weather_response(weather_data: dict) -> str:
    """
    Format weather data into a readable string.
    
    Args:
        weather_data: Dictionary containing weather information
        
    Returns:
        Formatted weather string
    """
    if "error" in weather_data:
        return weather_data["error"]
    
    return f"""Weather in {weather_data['city']}, {weather_data['country']}:
- Temperature: {weather_data['temperature']}°C (feels like {weather_data['feels_like']}°C)
- Conditions: {weather_data['description'].capitalize()}
- Humidity: {weather_data['humidity']}%
- Wind Speed: {weather_data['wind_speed']} m/s"""
