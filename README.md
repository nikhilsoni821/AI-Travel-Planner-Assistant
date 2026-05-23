# AI-Travel-Planner-Assistant
"An Agentic AI-powered travel planning assistant built with LangChain, Streamlit, and Gemini AI. It generates real-time, customized day-wise itineraries, including flights, hotels, and budget analysis."
# ✈️ Agentic AI-Based Travel Planning Assistant Using LangChain

An intelligent, autonomous travel planning application powered by **LangChain**, **Gemini AI**, and **Streamlit**. This agentic AI assistant acts as a professional travel planner, taking user preferences (source, destination, budget, and days) to generate a structured, real-time, and highly practical travel itinerary.

---

## 🌟 Key Features

*   **🧠 Agentic AI Logic:** Utilizes LangChain's autonomous agents to independently search, analyze, and structure travel data.
*   **🌐 Real-Time Data Integration:** Capable of fetching live data for flights, hotels, and weather conditions using integrated custom tools.
*   **📊 Progressive Disclosure UI:** A clean, modern Streamlit interface that organizes heavy data into readable formats using Tabs, Metrics, and Expanders.
*   **💰 Budget Tracking:** Monitors the user's specified budget and provides cost-effective travel recommendations.
*   **📅 Day-Wise Itinerary:** Generates a detailed, day-by-day schedule including activities, transport, and dining suggestions.

---

## 📁 Project Structure

```text
📂 travel-planning-assistant
 ┣ 📂 agents
 ┃ ┗ 📜 travel_agent.py      # Core LangChain Agent logic
 ┣ 📂 utils
 ┃ ┗ 📜 data_search.py       # Custom tools for flights, hotels, weather
 ┣ 📜 app.py                 # Main Streamlit UI file
 ┣ 📜 requirements.txt       # Project dependencies
 ┣ 📜 .env.example           # Example environment variables file
 ┗ 📜 README.md              # Project documentation
```

---

## 🚀 Step-by-Step Installation & Setup

Follow these exact commands in your terminal to set up and run the project locally.

### 1. Prerequisites
Make sure you have **Python 3.8+** installed on your system. You can check your Python version by running:
```bash
python --version
```

### 2. Clone the Repository
Clone this project to your local machine:
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
```
*(Note: Replace `your-username` and `your-repo-name` with your actual GitHub details).*

### 3. Create and Activate a Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies.

**For Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**For macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Required Dependencies
Once the virtual environment is activated, install all the required Python packages:
```bash
pip install -r requirements.txt
```

*(Make sure your `requirements.txt` includes at least the following packages:)*
```text
streamlit
langchain
langchain-google-genai
python-dotenv
```

### 5. Set Up Environment Variables
Create a file named `.env` in the root folder of the project. Add your API keys to this file. 

```env
# .env file
GEMINI_API_KEY=your_google_gemini_api_key_here
```
*Never share or commit your `.env` file to GitHub.*

### 6. Run the Application
Finally, start the Streamlit server using the following command:
```bash
streamlit run app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`.

---

## 🖥️ How to Use the App

1. **Enter Details:** Open the sidebar and enter your Departure City, Destination City, Total Budget, and Trip Duration.
2. **Add Preferences:** Fill in the optional "Special Preferences" box (e.g., "Vegetarian food only", "focus on historical places").
3. **Plan Itinerary:** Click the **"Plan My Itinerary"** button.
4. **View Results:** The AI Agent will process the real-time data and display your personalized trip snapshot along with organized tabs for **Flights, Hotels, Itinerary, and Budget**.

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

---
**Built with ❤️ by Nikhil using Python, LangChain, Gemini AI, and Streamlit.**
