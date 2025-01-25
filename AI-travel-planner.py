import google.generativeai as genai
import streamlit as st

# Configure Gemini API key
genai.configure(api_key="AIzaSyAaP6FLcEXSFWUmh44zRUr2fBx-K0UQ7f4")

# Application Title
st.title("🌍 AI-Powered Travel Itinerary Planner")

# Step 1: Gather User Inputs
with st.sidebar:
    st.header("Plan Your Trip")
    destination = st.text_input(
        "📍 Destination:", 
        placeholder="Enter your destination (e.g., Paris, Tokyo)", 
        help="Specify the city or country you want to visit."
    )
    duration = st.number_input(
        "⏳ Trip Duration (in days):", 
        min_value=1, 
        max_value=10, 
        step=1, 
        help="Enter the total number of days for your trip (1-10)."
    )
    budget = st.selectbox(
        "💰 Budget:", 
        ["Low", "Moderate", "High"], 
        help="Choose the budget range that best suits your trip."
    )
    purpose = st.selectbox(
        "🎯 Purpose:", 
        ["Leisure", "Business", "Adventure", "Cultural Exploration", "Other"], 
        help="Select the primary reason for your trip."
    )
    preferences = st.text_area(
        "🎨 Preferences:", 
        placeholder="E.g., food, adventure, culture", 
        help="Describe your preferences briefly, such as activities or experiences you enjoy."
    )
    dietary = st.text_input(
        "🥗 Dietary Preferences:", 
        placeholder="E.g., vegetarian, non-veg, both", 
        help="Mention any specific dietary requirements or restrictions."
    )
    interests = st.text_area(
        "🧭 Interests:", 
        placeholder="E.g., trekking, museums, local markets", 
        help="List activities or places of interest you'd like to explore."
    )
    mobility = st.selectbox(
        "🚶 Mobility Concerns:", 
        ["None", "Mild", "Moderate", "Severe"], 
        help="Indicate if you have any mobility constraints to consider."
    )
    accommodation = st.selectbox(
        "🏨 Accommodation Type:", 
        ["Luxury", "Budget", "Central Location", "Eco-Friendly"], 
        help="Select the type of accommodation you prefer."
    )
    travel_mode = st.selectbox(
        "🚗 Travel Mode:", 
        ["Walking", "Public Transport", "Private Vehicle", "Mixed"], 
        help="Choose your preferred mode of transportation at the destination."
    )

# Step 2: Additional Details
st.header("Refine Your Itinerary")
additional_details = st.text_area(
    "Add any additional details for refinement:", 
    help="Provide any extra information or specific requests for your itinerary."
)

# Step 3: Generate Itinerary
if st.button("Generate Itinerary"):
    if not destination or not preferences or not purpose:
        st.error("❌ Please provide the destination, purpose, and preferences for your trip.")
    else:
        # Generate user input summary
        user_input = (
            f"You are an AI travel planner. Plan a {duration}-day trip to {destination} with a {budget} budget. "
            f"Purpose: {purpose}. Preferences: {preferences}. "
            f"Dietary preferences: {dietary}. Interests: {interests}. "
            f"Mobility concerns: {mobility}. Accommodation preference: {accommodation}. "
            f"Travel mode: {travel_mode}. Provide a structured and detailed daily itinerary for each day, ensuring activities align with the user's preferences. "
            f"Include top-rated attractions, hidden gems, and time for relaxation. "
            f"Additional details: {additional_details}."
        )
    with st.spinner("Generating your personalized itinerary..."):
        try:
            # Generate response using Gemini AI
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(user_input)

            st.subheader("Your Personalized Itinerary")

            raw_response = response.text
            # Format and display structured itinerary
            st.markdown("---")
            st.markdown(f"### **{duration}-Day Itinerary for {destination}**")
            st.markdown(f"**Budget:** {budget}\n**Purpose:** {purpose}\n**Accommodation Preference:** {accommodation}\n**Travel Mode:** {travel_mode}")

            # Reformat response into a conversational itinerary
            itinerary_lines = raw_response.split('\n')
            structured_itinerary = []
            current_day = 1
            day_content = []

            for line in itinerary_lines:
                if line.startswith("Day") and day_content:
                    structured_itinerary.append("\n".join(day_content))
                    day_content = [f"**Day {current_day}:**"]
                    current_day += 1
                day_content.append(line)

            if day_content:
                structured_itinerary.append("\n".join(day_content))

            if structured_itinerary:
                for itinerary in structured_itinerary:
                    st.markdown(itinerary)
            else:
                st.warning("The AI did not return a structured itinerary.")
                st.info("Here are some general suggestions for your trip:")
                st.write(f"- Explore famous landmarks in {destination}.")
                st.write("- Try local cuisines and hidden gems.")
                st.write("- Include time for relaxation and adventure based on your preferences.")
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
            st.warning("This could be due to the AI model configuration or network issues. Please try again later.")

st.markdown("---")
st.write("✨ *Powered by Gemini AI*")
