import json
import os
from langchain.tools import tool

# Set the data folder path for reliable file access
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

@tool
def search_flights(source: str, destination: str) -> str:
    """Use this tool to search for available flights from a source city to a destination city."""
    try:
        file_path = os.path.join(DATA_DIR, 'flights.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            flights_data = json.load(file)
        
        # Filter flights based on source and destination
        available_flights = [
            f for f in flights_data 
            if f.get('source', '').lower() == source.lower() 
            and f.get('destination', '').lower() == destination.lower()
        ]
        
        if not available_flights:
            return f"No flights found from {source} to {destination}."
        return json.dumps(available_flights)
    except Exception as e:
        return f"Error reading flights data: {str(e)}"

@tool
def search_hotels(city: str) -> str:
    """Use this tool to search for available hotels in a specific city."""
    try:
        file_path = os.path.join(DATA_DIR, 'hotels.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            hotels_data = json.load(file)
        
        # Filter hotels based on the selected city
        available_hotels = [
            h for h in hotels_data 
            if h.get('city', '').lower() == city.lower()
        ]
        
        if not available_hotels:
            return f"No hotels found in {city}."
        return json.dumps(available_hotels)
    except Exception as e:
        return f"Error reading hotels data: {str(e)}"

@tool
def search_places(city: str) -> str:
    """Use this tool to search for popular places to visit in a specific city."""
    try:
        file_path = os.path.join(DATA_DIR, 'places.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            places_data = json.load(file)
        
        available_places = [
            p for p in places_data 
            if p.get('city', '').lower() == city.lower()
        ]
        
        if not available_places:
            return f"No places found in {city}."
        return json.dumps(available_places)
    except Exception as e:
        return f"Error reading places data: {str(e)}"
