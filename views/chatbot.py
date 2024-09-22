import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image
import google.generativeai as genai
import PyPDF2
import io
import json

# Load environment variables from secrets.toml
load_dotenv()

# Retrieve and configure Google API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API key not found. Make sure it's set in secrets.toml.")
else:
    genai.configure(api_key=api_key)

# Function to load Generative AI model and get response
def get_gemini_response(input_text, file_content, input_prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input_text, file_content, input_prompt])
        return response.text if hasattr(response, 'text') else "No textual response received from the API."
    except Exception as e:
        return f"Error occurred: {str(e)}"

# Function to process the uploaded file (image or PDF)
def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        if file_extension in ['jpg', 'jpeg', 'png']:
            return [{"mime_type": uploaded_file.type, "data": uploaded_file.getvalue()}]
        elif file_extension == 'pdf':
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
            return "\n".join(page.extract_text() for page in pdf_reader.pages)
        else:
            raise ValueError("Unsupported file type. Please upload a PDF or image file.")
    else:
        raise FileNotFoundError("No file uploaded")

# Function to generate quiz questions
def generate_quiz(summary):
    quiz_prompt = f"""
    Based on the following summary, generate 5 multiple-choice questions to test understanding. 
    Each question should have 4 options (A, B, C, D) with one correct answer. 
    Format the output as a JSON string of a list of dictionaries, each with keys: 
    'question', 'options' (list of 4 strings), and 'correct_answer' (index 0-3).

    Summary: {summary}

    Example format:
    [
        {{
            "question": "What is the main topic?",
            "options": ["A", "B", "C", "D"],
            "correct_answer": 2
        }},
        ...
    ]
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(quiz_prompt)
        
        if hasattr(response, 'text'):
            try:
                quiz_questions = json.loads(response.text)
            except json.JSONDecodeError:
                start = response.text.find('[')
                end = response.text.rfind(']') + 1
                if start != -1 and end != -1:
                    quiz_questions = eval(response.text[start:end])
                else:
                    raise ValueError("Unable to parse the quiz questions")

            if not isinstance(quiz_questions, list) or len(quiz_questions) == 0:
                raise ValueError("Invalid quiz question format")

            for question in quiz_questions:
                if not all(key in question for key in ['question', 'options', 'correct_answer']):
                    raise ValueError("Invalid question format")
                if len(question['options']) != 4:
                    raise ValueError("Each question must have exactly 4 options")
                if not isinstance(question['correct_answer'], int) or question['correct_answer'] not in range(4):
                    raise ValueError("Invalid correct_answer")

            return quiz_questions
        else:
            raise ValueError("No text response received from the API")
    except Exception as e:
        st.error(f"Error generating quiz: {str(e)}")
        return []

# Initialize session state variables
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = None
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = None
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False

# Initialize Streamlit app
st.header("Document Summary and Quiz Application")

# Input prompt and file uploader
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose a file...", type=["pdf", "jpg", "jpeg", "png"])

# Display uploaded file
if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension in ['jpg', 'jpeg', 'png']:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)
    elif file_extension == 'pdf':
        st.success(f"PDF file '{uploaded_file.name}' uploaded successfully.")

# Button to submit the input and file
if st.button("Summarize and Generate Quiz"):
    try:
        file_content = process_uploaded_file(uploaded_file)
        input_prompt = """
        You are an expert in understanding documents.
        You will receive either an input image or text content from a PDF.
        Provide a comprehensive summary based on the input.
        """
        st.session_state.summary = get_gemini_response(input_prompt, file_content, input_text)
        st.session_state.quiz_questions = generate_quiz(st.session_state.summary)
        st.session_state.user_answers = [None] * len(st.session_state.quiz_questions)
        st.session_state.quiz_submitted = False
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Display summary and quiz if available
if st.session_state.summary:
    st.subheader("Document Summary")
    st.write(st.session_state.summary)

    if st.session_state.quiz_questions:
        st.subheader("Quiz")
        for i, question in enumerate(st.session_state.quiz_questions):
            st.write(f"\n{i+1}. {question['question']}")
            user_answer = st.radio(f"Select your answer for question {i+1}:", 
                                   options=question['options'], 
                                   key=f"q{i}",
                                   index=None)
            if user_answer:
                st.session_state.user_answers[i] = question['options'].index(user_answer)

        if st.button("Submit Quiz"):
            st.session_state.quiz_submitted = True

        if st.session_state.quiz_submitted:
            score = sum([1 for i, q in enumerate(st.session_state.quiz_questions) if st.session_state.user_answers[i] == q['correct_answer']])
            st.write(f"\nYour score: {score} out of {len(st.session_state.quiz_questions)}")
            
            for i, (question, user_answer) in enumerate(zip(st.session_state.quiz_questions, st.session_state.user_answers)):
                st.write(f"\nQuestion {i+1}: {question['question']}")
                if user_answer is not None:
                    st.write(f"Your answer: {question['options'][user_answer]}")
                else:
                    st.write("Your answer: Not answered")
                st.write(f"Correct answer: {question['options'][question['correct_answer']]}")
                if user_answer == question['correct_answer']:
                    st.write("Correct!")
                else:
                    st.write("Incorrect.")
    else:
        st.error("Failed to generate quiz questions. Please try again.")