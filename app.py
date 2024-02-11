# Step 1: Import Required Libraries
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Step 2: Load all the environment variables 
load_dotenv()

# Step 3: Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Step 4: Load Google Gemini Pro Vision API And get response
def get_gemini_repsonse(input_prompt,image):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input_prompt,image[0]])
    return response.text

# Step 5: Convert Input Image into required parts (mime_type, bytes_data)
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
# Step 6: Streamlit App
st.set_page_config(page_title="Nutritionist Generative AI Doctor")

st.header("Nutritionist Generative AI Doctor")
#input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me about my food")

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
        Finally you can mention whether the food is health or not and also mention the percentage split
        of the ratio of carbohydrates, fats, fibers, sugar, and other things required in our diet. 

"""
## If Button is clicked
if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data)
    st.subheader("Food Details:")
    st.write(response)
