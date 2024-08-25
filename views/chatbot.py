import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables from secrets.toml
load_dotenv()  # Ensure this points to the correct environment file if needed

# Retrieve and configure Google API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API key not found. Make sure it's set in secrets.toml.")
else:
    genai.configure(api_key=api_key)

# Function to load Generative AI model and get response
def get_gemini_response(input_text, image_data, input_prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input_text, image_data[0], input_prompt])
        
        # Safely extract text content from the response
        if hasattr(response, 'text'):
            return response.text
        else:
            return "No textual response received from the API."
    except Exception as e:
        return f"Error occurred: {str(e)}"

# Function to process the uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
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

# Initialize Streamlit app
st.header("Gemini Application")

# Input prompt and file uploader
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Button to submit the input and image
submit = st.button("Tell me about the image")

# Default input prompt for the model
input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image.
               """

# If the submit button is clicked
if submit:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, input_text)
        st.subheader("The Response is")
        st.write(response)
    except FileNotFoundError as e:
        st.error(f"Error: {e}")
