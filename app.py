import streamlit as st
import json
import yaml
import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')  # Ensure API Key is loaded

if not API_KEY:
    st.error("⚠ Google API key not found. Please check your .env file.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=API_KEY)

# Streamlit UI Configuration
st.set_page_config(page_title="AI-Powered Schema Selection for NL to SQL Pipelines", layout="wide")
st.title("📂 AI-Powered Schema Selection for NL to SQL Pipelines")

# Upload JSON/YAML file
uploaded_file = st.file_uploader("📂 Upload a JSON/YAML file containing the database schema", type=["json", "yaml", "yml"])

# User Input: Natural Language Query
nl_query = st.text_input("📝 Enter your natural language query:")

# Add an "Enter" button for query submission
submit_query = st.button("🔍 Enter")


def load_schema(file):
    """Loads JSON or YAML schema from the uploaded file."""
    try:
        content = file.read().decode("utf-8")
        if file.name.endswith(".yaml") or file.name.endswith(".yml"):
            return yaml.safe_load(content)  # Parse YAML
        else:
            return json.loads(content)  # Parse JSON
    except Exception as e:
        st.error(f"⚠ Error loading schema: {e}")
        return None


def clean_gemini_response(raw_text):
    """Cleans Gemini's response to extract valid JSON."""
    try:
        raw_text = raw_text.strip()

        # Remove markdown formatting (if present)
        raw_text = re.sub(r"```json|```", "", raw_text).strip()

        # Try parsing directly
        return json.loads(raw_text)

    except json.JSONDecodeError:
        st.error("⚠ Gemini response is not valid JSON. Trying auto-fix...")

        # Auto-fix common errors
        try:
            fixed_text = raw_text.replace("\n", "").replace("'", '"')  # Fix newlines & single quotes
            return json.loads(fixed_text)
        except json.JSONDecodeError:
            st.error("⚠ Auto-fix failed. Showing raw response for debugging:")
            st.code(raw_text, language="json")
            return None


def get_gemini_response(nl_query, schema):
    """Uses Gemini to analyze NL query and return relevant data values."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([
            "You are an AI that extracts relevant information from a database schema.",
            f"Schema (JSON format): {json.dumps(schema, indent=2)}",
            f"Query: {nl_query}",
            """Respond **only** in a strict JSON format, without extra text. The output should be:
            {
                "relevant_data": {
                    "table_name": [
                        {"column1": "value1", "column2": "value2", ...}
                    ]
                }
            }
            If the query asks for specific data (e.g., names of students), return those values instead of just column names.
            Ensure the JSON is valid and contains relevant data. Do not include explanations, markdown, or extra text."""
        ])
        
        if not response or not response.candidates:
            st.error("⚠ Gemini returned an empty response.")
            return None
        
        raw_text = response.text.strip()
        
        # Show Gemini's raw output for debugging
        st.subheader("📜 Debug: Gemini Raw Output")
        st.code(raw_text, language="json")

        return clean_gemini_response(raw_text)  # Ensure valid JSON

    except Exception as e:
        st.error(f"⚠ Error in Gemini processing: {e}")
        return None


# Process query only when "Enter" button is clicked
if submit_query and uploaded_file and nl_query:
    schema = load_schema(uploaded_file)
    
    if schema:
        relevant_data = get_gemini_response(nl_query, schema)

        if relevant_data:
            st.subheader("📊 Extracted Data from Schema:")
            st.json(relevant_data, expanded=True)  # Display structured JSON output
        else:
            st.warning("⚠ No relevant data found.")
    else:
        st.error("⚠ Schema could not be loaded. Please check your file format.")
