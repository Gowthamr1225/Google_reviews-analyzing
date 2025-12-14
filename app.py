import streamlit as st
import requests
import os
import uuid

url = ""  # The complete API endpoint URL for this flow


headers = {
    "X-DataStax-Current-Org": "", 
    "Authorization": "Bearer <YOUR_APPLICATION_TOKEN>", 
    "Content-Type": "application/json", 
    "Accept": "application/json", 
    }

# ---- Function to call Langflow API ----
def analyze_review(input_value: str, url: str, headers: dict) -> str:
    payload = {
        "output_type": "chat",
        "input_type": "chat",
        "input_value": input_value,
        "session_id": str(uuid.uuid4())
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        outputs = data.get("outputs", [])
        if outputs and "results" in outputs[0]["outputs"][0]:
            return outputs[0]["outputs"][0]["results"]["message"].get("text", "_No text found._")
        return "_No response from Langflow API._"
    except requests.exceptions.RequestException as e:
        return f"🚨 Network error: {e}"
    except ValueError:
        return "⚠️ Invalid JSON response from Langflow API."
    except Exception as e:
        return f"⚠️ Unexpected error: {e}"

# ---- Streamlit UI ----
st.title("🌟 Review Analyzer")
st.markdown("Enter details below and get an **LLM-generated markdown summary**!")

# Input fields
place_id = st.text_input("🏷️ Place ID", placeholder="Enter the place ID here...")
place_name = st.text_input("📍 Place Name", placeholder="Enter the place name here...")
review_input = st.text_area("📝 Review Text", placeholder="Type your review text here...")

# Analyze button
if st.button("Analyze Review"):
    if not (place_id.strip() or place_name.strip() or review_input.strip()):
        st.warning("⚠️ Please enter at least one field (Place ID, Place Name, or Review Text).")
    else:
        # Build input dynamically based on what was provided
        input_value = ""
        if place_id.strip():
            input_value += f"Place ID: {place_id}\n"
        if place_name.strip():
            input_value += f"Place Name: {place_name}\n"
        if review_input.strip():
            input_value += f"Review: {review_input}\n"

        # Call API
        output = analyze_review(input_value, url, headers)

        # Display result
        st.subheader(":blue[AI Output:]", divider="rainbow")
        st.write(output)
