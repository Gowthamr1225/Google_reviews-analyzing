import streamlit as st
import requests
import uuid
import os
from dotenv import load_dotenv

# --- SECURE API CONFIGURATION ---
# Load variables from the .env file
load_dotenv()

# Fetch the credentials securely
API_KEY = os.getenv("LANGFLOW_API_KEY")
API_URL = os.getenv("LANGFLOW_API_URL")

# --- PAGE CONFIG ---
st.set_page_config(page_title="Review Analyzer", layout="wide")
st.title("📊 Google Reviews Analyzer Dashboard")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ System Status")
    # Visually confirm the API key is loaded without revealing it
    if API_KEY and API_URL:
        st.success("✅ API Connected via .env")
    else:
        st.error("❌ Missing .env configuration. Please check your variables.")
        st.stop() # Stops the app from running if credentials are missing
        
    st.markdown("---")
    st.info("Agentic AI Pipeline: Active\nModel: Llama-3 70B (Groq)")

# --- MAIN UI: USER INPUT ---
st.write("Enter a Location Name or Place ID to analyze 2,000+ reviews.")
user_input = st.text_input("Location Name / Place ID", placeholder="e.g., Starbucks Times Square")

# --- ACTION BUTTON ---
if st.button("Run Analysis", type="primary"):
    
    if not user_input:
        st.warning("⚠️ Please enter a Location Name or Place ID.")
    else:
        with st.spinner(f"Agentic AI is processing reviews for {user_input}..."):
            
            # 1. Setup API Request
            payload = {
                "output_type": "chat",
                "input_type": "chat",
                "input_value": user_input,
                "session_id": str(uuid.uuid4())
            }
            headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
            
            try:
                # 2. Make the API Call
                response = requests.post(API_URL, json=payload, headers=headers)
                response.raise_for_status() 
                
                # 3. Extract Langflow Response
                try:
                    result_text = response.json()['outputs'][0]['outputs'][0]['results']['message']['text']
                except (KeyError, IndexError):
                    # Fallback just in case the Langflow output structure changes slightly
                    result_text = "Failed to extract exact message. Raw response:\n\n" + str(response.json())
                
                st.success("✅ Analysis Complete!")
                st.divider()

                # --- TEXT/MARKDOWN RESULTS ---
                # This will render the AI's markdown tables, bold text, and lists perfectly
                st.markdown(result_text)

            except requests.exceptions.RequestException as e:
                st.error(f"❌ API Connection Error: {e}")