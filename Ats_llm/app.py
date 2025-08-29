import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to query Gemini
def get_gemini_response(input_text):
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    response = model.generate_content(input_text)
    return response.text

# Function to extract text from PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += str(page.extract_text())
    return text

# Prompt Template
input_prompt = """
Hey, act like a skilled and experienced ATS (Application Tracking System)
with a deep understanding of tech roles such as software engineering, data science,
data analytics, and big data engineering.

Your task is to evaluate the resume against the provided job description.
The job market is highly competitive, so provide the best guidance for resume improvement.

Assign a percentage match based on the JD and highlight missing keywords.
Return the result in **one single JSON string** with the structure:
{{
  "JD Match": "%",
  "MissingKeywords": [],
  "Profile Summary": ""
}}

Resume: {text}

Job Description: {jd}
"""

# Streamlit UI
st.title("Smart ATS")
st.text("Improve Your Resume ATS")

jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload a PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None and jd.strip() != "":
        text = input_pdf_text(uploaded_file)

        # Format prompt with actual JD and Resume text
        final_prompt = input_prompt.format(text=text, jd=jd)

        response = get_gemini_response(final_prompt)
        st.subheader("ATS Evaluation Result")
        st.write(response)

    else:
        st.warning("Please provide both a Job Description and a Resume PDF.")
