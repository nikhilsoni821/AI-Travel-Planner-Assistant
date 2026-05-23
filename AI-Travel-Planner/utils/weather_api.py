import requests

def get_weather(city: str) -> dict:
    """
    Function to fetch live weather for any city using the free wttr.in service.
    No API key is required for this service.
    """
    try:
        # Fetch the weather report from wttr.in in JSON format
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract the required weather details
            current = data['current_condition'][0]
            temp_c = current['temp_C']
            weather_desc = current['weatherDesc'][0]['value']
            humidity = current['humidity']
            wind_speed = current['windspeedKmph']
            
            full_info = f"Current Temperature: {temp_c}Â°C, Condition: {weather_desc}, Humidity: {humidity}%, Wind Speed: {wind_speed} km/h."
            
            return {
                "status": "success",
                "temp": temp_c,
                "description": weather_desc,
                "full_info": full_info
            }
        else:
            return {"status": "error", "full_info": "Weather service temporarily unreachable."}
            
    except Exception as e:
        return {"status": "error", "full_info": f"Could not fetch live weather: {str(e)}"}
