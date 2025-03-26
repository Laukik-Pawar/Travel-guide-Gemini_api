import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set up Gemini API
api_key = os.getenv("GEMINI_API_KEY") # Replace with your actual API key

if not api_key:
    st.error("API key not found. Please set GEMINI_API_KEY in your environment.")
else:
    genai.configure(api_key=api_key)
def generate_itinerary(destination, duration, budget, activities, preferences, mode_of_arrival, mode_of_departure):
    """Generate a structured travel itinerary using Gemini AI."""
    prompt = f"""
    You are a travel assistant. Create a {duration}-day itinerary for {destination}.
    Budget: {budget}.
    activities: {activities} if available in city.
    Preferences: {preferences}
    Ensure variety in activities such as sightseeing, food, culture, and adventure.  (Be prcise while stating hotels and restaurants when asked, 
    also state modes of transport and where we can get what mode of transport,give suggestions as per {mode_of_arrival} which states all about arrival detail and {mode_of_departure} which states all about arrival detail , 
    give approxiamte final budget along with expenses for all activities, summarize later in bullet points,  )
    """

    model = genai.GenerativeModel("gemini-1.5-pro-latest")  # Use latest model
    response = model.generate_content(prompt)
    return response.text if response.text else "Could not generate an itinerary."

def main():
    st.title("🌍 AI Travel Planner with Gemini")
    st.write("Plan your trip with AI-powered recommendations! 🚀")

    # User Inputs
    destination = st.text_input("Enter your destination:")
    duration = st.number_input("Number of days:", min_value=1, max_value=30, step=1)
    budget = st.selectbox("Budget Level:", ["Low", "Medium", "High"])
    activities = st.text_area("What type of activities do you prefer?")
    preferences = st.text_area("What type of experiences do you prefer?")
    mode_of_arrival = st.text_area("What type of mode of transport do you prefer for arrival and at what time(also mention precise point of arrival if applicable)")
    mode_of_departure = st.text_area("What type of mode of transport do you prefer for departure and at what time(also mention precise point from where you will depart if applicable)")

    if st.button("Generate Itinerary"):
        if destination and duration and budget and preferences:
            itinerary = generate_itinerary(destination, duration, budget, activities, preferences, mode_of_arrival, mode_of_departure )
            st.subheader("Your Travel Itinerary:")
            st.write(itinerary)
        else:
            st.error("Please fill in all fields before generating the itinerary.")

if __name__ == "__main__":
    main()
