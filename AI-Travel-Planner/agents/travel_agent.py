import os
import json
import re
from dotenv import load_dotenv

# Core LangChain ecosystem imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Custom modules from the utils folder
from utils.data_search import search_flights, search_hotels
from utils.weather_api import get_weather

# Load environment variables
load_dotenv()

# 1. Core LLM Setup
# Stable model initialization line
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

# 2. DATA ORCHESTRATION PIPELINE
def execute_travel_tools(inputs: dict) -> dict:
    query = inputs.get("user_query", "")
    
    # For strict LangChain prompt-based text extraction
    extraction_prompt = PromptTemplate.from_template(
        "Extract the source city and destination city from this text: '{query}'. "
        "You must respond ONLY with a JSON object containing 'source' and 'destination' keys.\n"
        "Example format: {{\"source\": \"Delhi\", \"destination\": \"Ranchi\"}}"
    )
    
    # Clean text-based extraction chain
    extraction_chain = extraction_prompt | llm | StrOutputParser()
    
    # Robust Python Parsing (Strictly checks for Markdown structures)
    try:
        raw_output = extraction_chain.invoke({"query": query}).strip()
        
        # Extract only the JSON block {} from the generated text using regex
        json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
        if json_match:
            clean_json_str = json_match.group(0)
            cities = json.loads(clean_json_str)
        else:
            cities = json.loads(raw_output)
            
        source = cities.get("source", "Delhi")
        destination = cities.get("destination", "Ranchi")
    except Exception:
        # Fallback values for safe execution
        source = "Delhi"
        destination = "Ranchi"

    # Actual Tools Execution
    flights = search_flights.invoke({"source": source, "destination": destination})
    hotels = search_hotels.invoke({"city": destination})
    
    # LIVE WEATHER API EXECUTION WITH SAFE CHECK
    try:
        weather_res = get_weather(destination)
        if isinstance(weather_res, dict) and weather_res.get("status") == "success":
            weather = weather_res.get("full_info")
        elif isinstance(weather_res, dict):
            weather = weather_res.get("full_info", str(weather_res))
        else:
            weather = str(weather_res)
    except Exception:
        weather = "Live weather data is currently unavailable, assume pleasant climate."
    
    return {
        "user_query": query,
        "flight_data": flights,
        "hotel_data": hotels,
        "weather_data": weather,
        "source": source,
        "destination": destination
    }

# 3. EXTENSIVE PROMPT TEMPLATE (Includes premium response structure)
final_planner_prompt = PromptTemplate.from_template(
    """You are a senior, highly sophisticated AI Travel Consultant powered by LangChain framework. 
    Analyze the gathered real-time constraints and curate an elite travel dashboard and itinerary.

    Trip Parameters:
    - User Request & Budget Context: {user_query}
    - Logistics / Available Flights (From {source} to {destination}): {flight_data}
    - Hospitality / Hotel Options in {destination}: {hotel_data}
    - LIVE Destination Weather Report: {weather_data}

    Formulate a comprehensive response structured with the following exact sections:
    
    ## âœˆï¸ Flight & Transport Analytics
    [Provide optimal flight recommendations based on the data, including explicit pricing details]
    
    ## ðŸ¨ Hotel & Stay Analysis
    [Curate hotel choices extracted from the structured data with features and costs]
    
    ## ðŸŒ¤ï¸ Live Weather Insights & Smart Packing List
    [Display the current live weather metrics provided above. Based on this climate, give a tailored packing list of essentials the user must carry]
    
    ## ðŸ’° Smart Cost Estimation & Budget Alert
    [Calculate an aggregate approximate cost breakdown for transport + stay and verify if it aligns with the user's intent]
    
    ## ðŸ—ºï¸ Day-by-Day Comprehensive Itinerary
    [A highly detailed chronological schedule mapping daily activities, tourist spots, and recommended culinary stops]

    Maintain an articulate, professional tone. Rely solely on provided facts and data points."""
)

# 4. THE ULTIMATE LANGCHAIN EXPRESSION LANGUAGE (LCEL) CHAIN
travel_agent_chain = (
    RunnablePassthrough() 
    | execute_travel_tools 
    | final_planner_prompt 
    | llm 
    | StrOutputParser()
)

# Main entrypoint function for app.py
def run_travel_agent(user_query: str):
    try:
        return travel_agent_chain.invoke({"user_query": user_query})
    except Exception as e:
        return f"An error occurred within the LangChain processing framework: {str(e)}"
