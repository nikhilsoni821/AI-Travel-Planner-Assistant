import re
import streamlit as st
from agents.travel_agent import run_travel_agent


def _map_section_key(section_title: str) -> str:
    title = section_title.lower()
    if "flight" in title or "transport" in title:
        return "flights"
    if "hotel" in title or "stay" in title or "hospitality" in title:
        return "hotels"
    if "weather" in title or "packing" in title:
        return "weather"
    if "budget" in title or "cost" in title:
        return "budget"
    if "day-by-day" in title or "itinerary" in title or "schedule" in title:
        return "itinerary"
    return "other"


def _extract_sections(plan_text: str) -> dict:
    sections = {
        "flights": "",
        "hotels": "",
        "weather": "",
        "budget": "",
        "itinerary": "",
        "other": "",
    }

    heading_pattern = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
    matches = list(heading_pattern.finditer(plan_text))

    if not matches:
        sections["itinerary"] = plan_text.strip()
        return sections

    for index, match in enumerate(matches):
        section_title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(plan_text)
        section_body = plan_text[start:end].strip()
        section_key = _map_section_key(section_title)

        if section_body:
            if sections[section_key]:
                sections[section_key] += "\n\n" + section_body
            else:
                sections[section_key] = section_body

    if not sections["itinerary"]:
        sections["itinerary"] = plan_text.strip()

    return sections


def _extract_daywise_items(itinerary_text: str) -> list:
    day_header_pattern = re.compile(
        r"(?im)^\s*(?:[-*]\s*)?(?:#{1,6}\s*)?(?:\*\*)?\s*(day\s*\d+)"
        r"(?:\s*[:\-|]\s*(.*))?(?:\*\*)?\s*$"
    )
    matches = list(day_header_pattern.finditer(itinerary_text))

    day_items = []
    for index, match in enumerate(matches):
        day_label = re.sub(r"\s+", " ", match.group(1)).strip().title()
        inline_summary = (match.group(2) or "").strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(itinerary_text)
        chunk = itinerary_text[start:end].strip()
        details = f"{inline_summary}\n\n{chunk}".strip() if inline_summary else chunk

        if details:
            day_items.append((day_label, details))

    return day_items


def _render_trip_snapshot(trip_meta: dict) -> None:
    st.markdown("### Trip Snapshot")
    col1, col2, col3 = st.columns(3)
    col1.metric("Destination", trip_meta.get("destination", "Not Available"))
    col2.metric("Duration", f"{trip_meta.get('days', 0)} Days")
    col3.metric("Budget", f"INR {trip_meta.get('budget', 0):,.0f}")


def _render_detailed_tabs(sections: dict, trip_meta: dict) -> None:
    flights_tab, hotels_tab, itinerary_tab, budget_tab = st.tabs(
        ["Flights", "Hotels", "Itinerary", "Budget"]
    )

    with flights_tab:
        st.markdown("#### Flight Details")
        st.markdown(sections["flights"] or "No flight details were generated for this request.")

    with hotels_tab:
        st.markdown("#### Hotel Details")
        st.markdown(sections["hotels"] or "No hotel details were generated for this request.")

    with itinerary_tab:
        st.markdown("#### Itinerary Overview")
        if sections["weather"]:
            st.markdown("##### Live Weather and Packing Guidance")
            st.markdown(sections["weather"])
            st.markdown("---")

        day_items = _extract_daywise_items(sections["itinerary"])
        if day_items:
            for day_label, day_details in day_items:
                with st.expander(day_label, expanded=False):
                    st.markdown(day_details)
        else:
            st.markdown(sections["itinerary"] or "No itinerary details were generated for this request.")

    with budget_tab:
        st.markdown("#### Budget Summary")
        st.metric("User Budget", f"INR {trip_meta.get('budget', 0):,.0f}")
        st.markdown(sections["budget"] or "No budget analysis was generated for this request.")


# 1. Page configuration
st.set_page_config(
    page_title="AI Travel Assistant",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 4rem; 
            padding-bottom: 2rem;
        }
        .app-title {
            font-size: 1.9rem;
            font-weight: 700;
            line-height: 1.4;
            margin-top: 1rem;
            margin-bottom: 0.5rem;
            white-space: normal;
            overflow: visible;
            text-overflow: clip;
            overflow-wrap: anywhere;
            word-break: break-word;
        }
        .app-subtitle {
            color: #4a4a4a;
            margin-bottom: 1.5rem;
        }
        @media (max-width: 768px) {
            .app-title {
                font-size: 1.45rem;
                line-height: 1.3;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 2. Main title and subtitle
st.markdown(
    "<div class='app-title'>✈️Agentic AI-Based Travel Planning Assistant Using LangChain</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='app-subtitle'>A professional travel assistant that uses real-time inputs to generate practical and structured trip plans.</div>",
    unsafe_allow_html=True,
)
st.markdown("---")

# 3. Sidebar setup for user inputs 
st.sidebar.header("Enter Trip Details")

source = st.sidebar.text_input("🛫Departure City (Source)", placeholder="e.g., Delhi")
destination = st.sidebar.text_input("📍Destination City", placeholder="e.g., Ranchi")
budget = st.sidebar.number_input("Total Budget (in INR)💵", min_value=1000, value=15000, step=500)
days = st.sidebar.slider("⏳Trip Duration (in days)", min_value=3, max_value=7, value=4)

preferences = st.sidebar.text_area(
    "Special Preferences (Optional)",
    placeholder="e.g., Vegetarian food only, 5-star hotels only, focus on historical places",
)

if "latest_itinerary" not in st.session_state:
    st.session_state.latest_itinerary = ""
if "latest_trip_meta" not in st.session_state:
    st.session_state.latest_trip_meta = {}

# 4. Action button and AI logic integration
if st.sidebar.button("📋Plan My Itinerary"):
    # Validate that required fields are provided
    if not source or not destination:
        st.error("Please enter valid names for both 'Source' and 'Destination' cities.")
    else:
        # Show a loading spinner while the AI processes the request
        with st.spinner(
            "The AI agent is analyzing flights, hotels, and live weather data. Please wait..."
        ):
            # Build a clear query for the AI agent
            user_query = (
                f"Create a detailed {days}-day trip itinerary from {source} to {destination}. "
                f"The total budget is {budget} INR. Additional user preferences: {preferences}. "
                f"Make sure to search flights, hotels, and weather using your tools."
            )

            # Run the agent and retrieve the response
            final_itinerary = run_travel_agent(user_query)
            st.session_state.latest_itinerary = final_itinerary
            st.session_state.latest_trip_meta = {
                "source": source,
                "destination": destination,
                "budget": budget,
                "days": days,
                "preferences": preferences,
            }

if st.session_state.latest_itinerary:
    st.success("Your customized travel plan is ready.")
    trip_meta = st.session_state.latest_trip_meta
    sections = _extract_sections(st.session_state.latest_itinerary)

    _render_trip_snapshot(trip_meta)
    st.markdown("---")
    _render_detailed_tabs(sections, trip_meta)

# 5. Footer 
st.markdown(
    "<br><hr><center><p style='color:gray;'>Built with ❤️ using LangChain, Gemini AI, and Streamlit</p></center>",
    unsafe_allow_html=True,
)