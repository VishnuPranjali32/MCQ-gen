import streamlit as st
import base64

# Set background image using base64-encoded CSS (JPG version)
def set_background(image_file):
    with open(image_file, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: contain;
        background-repeat: repeat;
        background-position: center;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Call background function with your .jpg file
set_background("BookDoodle.jpg")

# Main Title
st.markdown("## MCQ Generator")
st.markdown("### Unleash Your Learning Potential with AI-Powered MCQs")
st.markdown(
    "Generate engaging and challenging multiple-choice questions effortlessly. "
    "Whether you’re a student preparing for exams or an educator creating assessments, "
    "this tool helps you create customized quizzes in seconds, saving you time and enhancing your learning experience."
)

# Form to handle inputs
with st.form("mcq_form"):
    input_type = st.radio("Select input type:", ["Topic", "Text"])
    user_input = st.text_input("Enter a topic (e.g., Python Programming):") if input_type == "Topic" else st.text_area("Paste your content here:")
    num_questions = st.selectbox("Number of Questions", list(range(1, 11)))  # No parentheses
    num_options = st.selectbox("Number of Options", list(range(2, 6)))
    difficulty = st.radio("Difficulty level:", ["Easy", "Medium", "Hard"])
    submit = st.form_submit_button("Generate MCQs")

# When the user submits the form
if submit:
    st.success(f"Generating {num_questions} MCQs based on your {'topic' if input_type == 'Topic' else 'text'}...")
    for i in range(1, num_questions + 1) and range(2,num_options+1):
        st.markdown(f"**Q{i}:** This is a sample MCQ question.\n- A) Option 1\n- B) Option 2\n- C) Option 3\n- D) Option 4")
