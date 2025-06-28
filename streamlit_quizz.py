import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai

# --- GEMINI SETUP ---
GEMINI_API_KEY = "AIzaSyDYTaCduaqw6lj-NbhiKhsvLywaABCjCH4"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# --- HELPER FUNCTIONS ---

def extract_text_from_pdf(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
        return text.strip()
    except Exception as e:
        return f"Failed to extract from PDF: {e}"

def get_quizz_from_gemini(topic, text, level):
    prompt = f"Generate 10 quiz questions(mcq) on the following:\nTopic: {topic}\nLevel: {level}\nContent: {text}. \n\n note: 1)Only return quetions 2) after last quetion , create answer scetion : answer of each quetions"
    response = model.generate_content(prompt)
    return response.text

def get_quizz_from_text(text, level):
    prompt = f"Generate 10 quiz questions(mcq) from this text:\nLevel: {level}\n\n{text} \n\n note: 1)Only return quetions 2) after last quetion , create answer scetion : answer of each quetions"
    response = model.generate_content(prompt)
    return response.text

# --- STREAMLIT UI CONFIG ---
st.set_page_config(page_title="Quiz Generator", layout="wide")

# --- PAGE SELECTION ---
page = st.sidebar.selectbox("Select Page", ["From Topic + Content", "From PDF File"])

# --- PAGE 1: From Topic and Optional Content ---
if page == "From Topic + Content":
    st.header("📘 Generate Quiz from Topic")
    topic = st.text_input("Enter Topic:")
    content = st.text_area("Enter Content related to topic ( Optional )( Leave blank to rely on topic only ):")
    level = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
    
    if st.button("Generate Quiz"):
        if not topic:
            st.error("Please enter a topic.")
        else:
            result = get_quizz_from_gemini(topic, content, level)
            st.text_area("Generated Quiz", result, height=400)

# --- PAGE 2: From PDF ---
elif page == "From PDF File":
    st.header("📄 Generate Quiz from PDF File")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    level = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
    
    if st.button("Generate Quiz") and uploaded_file:
        pdf_text = extract_text_from_pdf(uploaded_file)
        if pdf_text:
            quiz = get_quizz_from_text(pdf_text, level)
            st.text_area("Generated Quiz", quiz, height=400)
        else:
            st.error("Could not extract text from PDF.")