import requests
from config import Config

def get_current_weather():
    url = Config.WEATHER_API_URL
    params = {
        'key': Config.WEATHER_API_KEY,
        'q': Config.WEATHER_LOCATION
    }
    
    try:
        response = requests.get(url, params=params)

        print("Status Code:", response.status_code)
        print("Raw Response:", response.text)
        print("Response Headers:", response.headers)

        if response.status_code == 200:
            try:
                return response.json()
            except ValueError as e:
                print(f"Error parsing JSON: {e}")
                print("Response content:", response.text)
                return None
        else:
            response.raise_for_status()  # Raise error for non-200 status codes
            
    except requests.exceptions.RequestException as e:
        print(f"Error accessing weather API: {e}")
        return None

# Test the function
result = get_current_weather()
if result:
    print("Parsed JSON:", result)