import google.generativeai as genai
import streamlit as st

# Configure Gemini API key (Ensure it's valid)
API_KEY = "YOUR_VALID_GEMINI_API_KEY"
genai.configure(api_key=API_KEY)

# Get available models dynamically
def get_available_model():
    try:
        models = genai.list_models()
        for model in models:
            if "gemini" in model.name:  # Use the latest available Gemini model
                return model.name
        return None  # No valid model found
    except Exception as e:
        st.error(f"⚠️ Error fetching available models: {e}")
        return None

MODEL_NAME = get_available_model()
if MODEL_NAME is None:
    st.error("❌ No valid Gemini model found. Please check your API key or account access.")

# Application Title
st.title("🌍 AI-Powered Travel Itinerary Planner")

# Step 1: Gather User Inputs
with st.sidebar:
    st.header("Plan Your Trip")
    destination = st.text_input("📍 Destination:", placeholder="Enter a city or country")
    duration = st.number_input("⏳ Trip Duration (days):", min_value=1, max_value=30, step=1)
    budget = st.selectbox("💰 Budget:", ["Low", "Moderate", "High"])
    purpose = st.selectbox("🎯 Purpose:", ["Leisure", "Business", "Adventure", "Cultural Exploration", "Other"])
    preferences = st.text_area("🎨 Preferences:", placeholder="E.g., food, adventure, culture")
    dietary = st.text_input("🥗 Dietary Preferences:", placeholder="E.g., vegetarian, non-veg, both")
    interests = st.text_area("🧭 Interests:", placeholder="E.g., trekking, museums, local markets")
    mobility = st.selectbox("🚶 Mobility Concerns:", ["None", "Mild", "Moderate", "Severe"])
    accommodation = st.selectbox("🏨 Accommodation Type:", ["Luxury", "Budget", "Central Location", "Eco-Friendly"])
    travel_mode = st.selectbox("🚗 Travel Mode:", ["Walking", "Public Transport", "Private Vehicle", "Mixed"])

# Step 2: Additional Details
st.header("Refine Your Itinerary")
additional_details = st.text_area("Any extra details? (Optional)")

# Step 3: Generate Itinerary
if st.button("Generate Itinerary"):
    if not destination or not preferences or not purpose:
        st.error("❌ Please provide the destination, purpose, and preferences for your trip.")
    elif MODEL_NAME is None:
        st.error("❌ No valid AI model available. Try again later.")
    else:
        user_input = (
            f"You are an AI travel planner. Plan a {duration}-day trip to {destination} with a {budget} budget. "
            f"Purpose: {purpose}. Preferences: {preferences}. "
            f"Dietary preferences: {dietary}. Interests: {interests}. "
            f"Mobility concerns: {mobility}. Accommodation preference: {accommodation}. "
            f"Travel mode: {travel_mode}. Provide a structured, detailed daily itinerary. "
            f"Include top attractions, hidden gems, and relaxation time. "
            f"Additional details: {additional_details}."
        )

        with st.spinner("Generating your personalized itinerary..."):
            try:
                # Generate response using Gemini AI
                model = genai.GenerativeModel(MODEL_NAME)
                response = model.generate_content(user_input)

                st.subheader("Your Personalized Itinerary")

                if response and hasattr(response, 'text'):
                    raw_response = response.text
                    st.markdown("---")
                    st.markdown(f"### **{duration}-Day Itinerary for {destination}**")
                    st.markdown(f"**Budget:** {budget}\n**Purpose:** {purpose}\n**Accommodation:** {accommodation}\n**Travel Mode:** {travel_mode}")

                    # Display structured itinerary
                    st.markdown(raw_response)
                else:
                    st.warning("⚠️ AI did not return a structured itinerary.")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
                st.warning("Please check your API key, model availability, or network connection.")

st.markdown("---")
st.write("✨ *Powered by Gemini AI*")
