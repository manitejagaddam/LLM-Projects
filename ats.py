import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
from pdf2image.exceptions import PDFInfoNotInstalledError
import google.generativeai as genai

# Configure Generative AI API
API_KEY = '' #please enter your API key 
genai.configure(api_key=API_KEY)

def get_gemini_response(input_text, pdf_content, prompt):
    """
    Generate a response using Gemini AI for the provided input, PDF content, and prompt.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def process_uploaded_pdf(uploaded_file):
    """
    Process the uploaded PDF file, converting the first page into an image.
    """
    if uploaded_file:
        try:
            images = pdf2image.convert_from_bytes(uploaded_file.read())
            first_page = images[0]

            img_byte_arr = io.BytesIO()
            first_page.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            return [{
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }]
        except PDFInfoNotInstalledError:
            st.error("Poppler is not installed. Please ensure it is properly installed and accessible.")
            raise
    else:
        raise FileNotFoundError("No file was uploaded.")

# Streamlit App Configuration
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# Job Description Input
job_description = st.text_area("Job Description:", key="input")

# File Upload
uploaded_file = st.file_uploader("Upload your resume (PDF format only):", type=["pdf"])
if uploaded_file:
    st.success("PDF Uploaded Successfully!")

# Prompts for Evaluation
prompt_review = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please provide a professional evaluation of whether the candidate's profile aligns with the role. Highlight the strengths and 
weaknesses of the applicant in relation to the specified job requirements.
"""

prompt_match = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Provide:
1. The percentage match of the resume to the job description.
2. The missing keywords.
3. Final thoughts on the alignment of the resume with the job description.
"""

# Buttons
if st.button("Tell Me About the Resume"):
    if uploaded_file:
        try:
            pdf_content = process_uploaded_pdf(uploaded_file)
            response = get_gemini_response(job_description, pdf_content, prompt_review)
            st.subheader("Response:")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload your resume.")

elif st.button("Percentage Match"):
    if uploaded_file:
        try:
            pdf_content = process_uploaded_pdf(uploaded_file)
            response = get_gemini_response(job_description, pdf_content, prompt_match)
            st.subheader("Response:")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload your resume.")
