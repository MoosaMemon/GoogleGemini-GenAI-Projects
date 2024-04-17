from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-pro-latest")

# input: Instructions for the model to behave in a certain way: "I want u to act as a.."
# prompt: Query of the user
def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")



st.set_page_config(page_title="Multi-language Invoice Extractor")
st.header("Invoice Extractor")

input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Upload image of the invoice: ", type=["jpg", "jpeg", "png"])

image = ""

if uploaded_file is not None:
    st.success("Image uploaded sucessfully!!")
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image.", use_column_width=True)
else:
    st.error("Image not uploaded!")

submit = st.button("Tell me about the invoice!")

input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image
               """


if submit:
    image_data = input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is: ")
    st.write(response)