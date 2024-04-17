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
def get_gemini_response(input_prompt, image):
    response = model.generate_content([input_prompt, image[0]])
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



st.set_page_config(page_title="Calorie Advisor - LIM based app")
st.header("Calorie Advisor")

uploaded_file = st.file_uploader("Upload image of the invoice: ", type=["jpg", "jpeg", "png"])

image = ""

if uploaded_file is not None:
    st.success("Image uploaded sucessfully!!")
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image.", use_column_width=True)
else:
    st.error("Image not uploaded!")

submit = st.button("Analyze my food intake!")

input_prompt = """
Task:  You are a highly skilled AI nutritionist trained in food identification and calorie estimation. Your primary function is to analyze images of food intake and generate the following:

Detailed Food Identification: Accurately list the specific food items present in each image (e.g., not just "salad," but "romaine lettuce, grilled chicken, tomatoes, croutons, Caesar dressing").

Precise Calorie Estimates: Calculate the approximate calorie count for each identified food item, taking into account portion sizes as visually interpreted from the image.

Total Meal Calories: Provide the cumulative calorie total for the entire image.

Health Insights: Offer a brief assessment of the food choices in the image. Highlight potential nutritional benefits and drawbacks (e.g., "This meal is a good source of protein and fiber, but consider reducing the dressing quantity for lower fat and calorie intake").

I will give you input in the below format.
Input: I will provide you with clear, well-lit images of meals and snacks throughout the day.

I want you to give me output in the Below format.
Output Format:



Item 1: [Food Name] ([Quantity, if discernible]) - [Estimated Calories]\n
Item 2: [Food Name] ([Quantity, if discernible]) - [Estimated Calories]\n
Item 3: ----\n
Item 4: ---\n



Total Meal Calories: [Total Calories]



The percentage split of the ratio of carbohydrates, fats, fibers, sugar, and other important things requied in our diet is as follows:

Carbohydrates: x%\n
Fats: x%\n
Fibers: x%\n
etc\n
etc\n



Health Insights: [Whether food is healthy or not, and brief analysis and suggestions]
"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt, image_data)
    st.subheader("The Response is: ")
    st.write(response)