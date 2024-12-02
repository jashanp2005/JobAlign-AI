import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Main UI
st.set_page_config(
    page_title="Smart ATS",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Sidebar
st.sidebar.title("Smart ATS")
st.sidebar.info("Optimize your resume for ATS and job descriptions. Upload your resume, paste the job description, and get instant feedback.")

# Header
st.title("📄 Smart ATS Assistant")
st.markdown(
    """
    **Welcome!** Improve your resume's match with job descriptions.
    Upload your resume (PDF) and paste the job description to receive a match percentage, missing keywords, and tips for improvement.
    """
)

# Job Description Input
jd = st.text_area(
    "📝 Paste the Job Description",
    placeholder="Paste the job description here...",
    help="Enter the job description from the job listing."
)

# Resume Upload
uploaded_file = st.file_uploader(
    "📤 Upload Your Resume",
    type="pdf",
    help="Upload your resume in PDF format."
)

# Submit Button
if st.button("🚀 Analyze My Resume"):
    if uploaded_file and jd.strip():
        # Display a progress spinner
        with st.spinner("Processing your resume and job description..."):
            text = input_pdf_text(uploaded_file)
            input_prompt = f"""
            Hey Act Like a skilled or very experience ATS(Application Tracking System) with a deep understanding of tech field,software engineering. 
            Your task is to evaluate the resume based on the given job description. You must consider the job market is very competitive and you should provide 
            best assistance for improving the resumes. Assign the percentage Matching based on Job description and the missing keywords with high accuracy  
            resume:{text} description:{jd} 
            I want the response in one single string having the structure  
            {{"Job Description Match":"%","MissingKeywords:[]","Profile Summary":""}} 
            """
            response = get_gemini_response(input_prompt)
        
        st.success("✅ Analysis Complete!")
        st.markdown("### 📊 Results")
        st.json(json.loads(response))  # Display the response as JSON for better readability
    else:
        st.warning("⚠️ Please upload a resume and paste a job description.")
