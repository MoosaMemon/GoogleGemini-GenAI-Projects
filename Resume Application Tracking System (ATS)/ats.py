# loading all of the necessary libraries
import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

# loading all of the enviroment variables
load_dotenv()

# setting the apy key in our google model
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

# function to initalize the genai model and get response
def get_gemini_repsonse(input, input_prompt):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content([input, input_prompt])
    return response.text

# function to extract text from pdf in order to feed to the gemini model (since google gemini only accepts text or images as input and not other file formats)
def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

# Prompt template to for ATS
input_prompt="""
Hey, act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field, software engineering, data science, data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on JD and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure as below
JD Match: %\n
MissingKeywords: []\n
Profile Summary: ""
"""

# Initalizing our streamlit app
st.set_page_config("HireWell - LLM Based ATS System.")
st.title("HireWell - Smart ATS")
st.subheader("Prioritizes beneficial placements for both sides.")

st.text("Improve your resume according to ATS!!")

jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the pdf")

if uploaded_file is not None:
    st.success("PDF uploaded sucessfully!!")
else:
    st.error("PDF not uploaded!!!")

submit1 = st.button("Resume percentage match with job description.")

if submit1:
    if uploaded_file is not None:

        text=input_pdf_text(uploaded_file)

        response=get_gemini_repsonse(text, input_prompt)

        st.write(response)
