import streamlit as st
import google.generativeai as genai
from google.generativeai import GenerativeModel

# --- UI Setup ---
st.set_page_config(page_title="PYQ AI Assistant 📝", page_icon="🧠", layout="centered")
st.title("PYQ AI Assistant 📝")
st.markdown("Easily generate similar questions and answer keys from any Previous Year Question (PYQ).")

# --- API Key Configuration ---
api_key = st.secrets.get("GEMINI_API_KEY", None)
if not api_key:
    st.error("API Key not found. Please add your 'GEMINI_API_KEY' to `.streamlit/secrets.toml`.")
    st.stop()

genai.configure(api_key=api_key)

# --- Load Gemini Model ---
model = GenerativeModel(model_name="gemini-1.5-pro-latest")

# --- Helper Functions ---
def generate_similar_question(original_question):
    prompt = f"Paraphrase this previous year question into a similar one:\n\n{original_question}"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating similar question: {e}")
        return None

def generate_answer_key(question):
    prompt = f"Provide a short answer key or marking scheme for this question:\n\n{question}"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating answer key: {e}")
        return None

# --- Input Section ---
user_pyq = st.text_area(
    "Enter a Previous Year Question (PYQ) here 👇",
    "What is the difference between a list and a tuple in Python?",
    height=150
)

# --- Generate Button ---
if st.button("Generate Similar Question and Answer Key 🚀"):
    if user_pyq.strip():
        with st.spinner("Generating..."):
            generated_question = generate_similar_question(user_pyq)
            generated_answer = generate_answer_key(user_pyq)

        if generated_question:
            st.subheader("🧠 Similar Question")
            st.info(generated_question)

        if generated_answer:
            st.subheader("🔑 Answer Key")
            st.success(generated_answer)
    else:
        st.warning("Please enter a question to continue.")
