import requests
from config import Config
import xml.etree.ElementTree as ET

def get_current_weather():
    """Fetch current weather data for configured location"""
    try:
        params = {
            'key': Config.WEATHER_API_KEY,
            'q': Config.WEATHER_LOCATION,
        }
        
        response = requests.get(Config.WEATHER_API_URL, params=params)
        response.raise_for_status()
        
        # Parse XML response
        root = ET.fromstring(response.content)
        
        # Extract weather data from XML
        current = root.find('current')
        weather_data = {
            'current': {
                'temp_c': float(current.find('temp_c').text),
                'temp_f': float(current.find('temp_f').text),
                'condition': {
                    'text': current.find('condition/text').text
                },
                'humidity': int(current.find('humidity').text),
                'wind_kph': float(current.find('wind_kph').text)
            }
        }
        
        return weather_data
        
    except Exception as e:
        print(f"Error fetching weather data: {str(e)}")
        return None

# Test the function
result = get_current_weather()
if result:
    print("Parsed JSON:", result)