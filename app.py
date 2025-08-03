import streamlit as st
import google.generativeai as genai
from google.generativeai import GenerativeModel

# --- 🎯 Core Features (Foundational) ---

## 4️⃣ Clean Streamlit UI
st.set_page_config(page_title="PYQ AI Assistant 📝", page_icon="🧠", layout="centered")

st.title("PYQ AI Assistant 📝")
st.markdown("Easily generate similar questions and answer keys from any Previous Year Question (PYQ).")


# --- Configure Google Gemini API ---
# Use st.secrets to access the API key securely from .streamlit/secrets.toml
try:
    genai.configure(api_key=st.secrets["AIzaSyAX7TGpaaiszs1Z3Rn1Dp4vXpFOPnk0MfU"])
except KeyError:
    st.error("API Key not found. Please add your 'GEMINI_API_KEY' to `.streamlit/secrets.toml`.")
    st.stop()

# Initialize the Gemini model. We'll use a single model for both tasks.
model = GenerativeModel(model_name="gemini-1.5-pro-latest")

# Function to generate a similar question
def generate_similar_question(original_question):
    prompt = f"Paraphrase the following previous year's question into a similar but distinct question: {original_question}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating similar question: {e}")
        return None

# Function to generate an answer key
def generate_answer_key(question):
    prompt = f"Provide a concise sample answer key or marking scheme for the following question: {question}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating answer key: {e}")
        return None


# 1️⃣ PYQ Input
user_pyq = st.text_area(
    "Enter a Previous Year Question (PYQ) here 👇",
    "What is the difference between a list and a tuple in Python?",
    height=150,
    help="Type in a question from a previous year's exam paper."
)

if st.button("Generate Similar Question and Answer Key 🚀"):
    if user_pyq:
        with st.spinner("Generating..."):
            # 2️⃣ Similar Question Generator
            generated_question = generate_similar_question(user_pyq)
            
            # 3️⃣ Answer Key Generator
            generated_answer = generate_answer_key(user_pyq)

        # --- Display results ---
        if generated_question:
            st.subheader("Generated Similar Question 🧠")
            st.info(generated_question)
        
        if generated_answer:
            st.subheader("Sample Answer Key 🔑")
            st.success(generated_answer)
    else:
        st.warning("Please enter a question to generate results.")