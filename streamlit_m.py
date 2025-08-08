import streamlit as st
from srcm.mcq_m import MCQGenerator
import json

def load_css(file_path):
    with open(file_path, "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

def display_mcq(i, mcq):
    st.markdown(f"**Question {i + 1}:** {mcq['question']}")
    if 'options' in mcq and isinstance(mcq['options'], list):
        for j, option in enumerate(mcq['options']):
            st.write(f"{chr(ord('A') + j)}. {option}")
        if 'correct_answer' in mcq:
            st.write(f"**Correct Answer:** {mcq['correct_answer']}")
        else:
            st.warning("Correct answer key missing.")
    else:
        st.error(f"Invalid 'options' format for question {i + 1}.")
    st.markdown("---")

def main():
    load_css("style.css")
    with st.container():
        st.markdown("## MCQ Generator")
        st.markdown("### Unleash Your Learning Potential with MCQ generator")
        st.markdown(
            "Generate engaging and challenging multiple-choice questions effortlessly. "
            "Whether you’re a student preparing for exams or an educator creating assessments, "
            "this tool helps you create customized quizzes in seconds, saving you time and enhancing your learning experience."
            )
        
        #Input options
        input_type = st.radio("Select input type:", ("Topic", "Text", "File"))
        uploaded_file = None
        if input_type == "Topic":
            input_text = st.text_input("Enter a topic: ")
        elif input_type == "Text":
            input_text = st.text_area("Enter text content:")
        elif input_type == "File":
            uploaded_file = st.file_uploader("Upload a file (PDF, DOCX, or PPTX):", type=["pdf", "docx", "pptx"])
            input_text = "" 
              
        num_questions = st.selectbox("Number of questions:", list(range(1, 11)), index=2) 
        num_options = st.selectbox("Number of options per question:", list(range(2, 6)), index=2)
        mode = st.radio("Difficulty Selection Mode:", ["Custom Counts", "Mixed Difficulty"])
        if mode == "Custom Counts":
            num_easy = st.number_input("Number of Easy questions:", min_value=0, value=2)
            num_medium = st.number_input("Number of Medium questions:", min_value=0, value=2)
            num_hard = st.number_input("Number of Hard questions:", min_value=0, value=1)
            total_questions = num_easy + num_medium + num_hard
            difficulty_config = {
                "easy": num_easy,
                "medium": num_medium,
                "hard": num_hard
                }
        else:
            total_questions = st.selectbox("Total number of questions:", list(range(1, 21)), index=4)
            difficulty_config = "mixed"
        
        if st.button("Generate"):
            if input_type == "File":
                from srcm.utils import extract_text_from_file
                if uploaded_file is not None:
                    input_text = extract_text_from_file(uploaded_file)
                else:
                    st.error("Please upload a valid file.")
                    return

    if not input_text:
        st.error("Please provide input.")
        return

    try:
        generator = MCQGenerator()
        result_str = generator.generate_mcqs(input_text, total_questions, num_options, difficulty_config)
        mcqs = json.loads(result_str)
        st.subheader(f"Generated MCQs ({min(num_questions, len(mcqs))} of {len(mcqs)}):")
        if isinstance(mcqs, list):
            for i, mcq in enumerate(mcqs[:num_questions]):
                display_mcq(i, mcq)
        else:
            st.error("Generated output is not a JSON list.")
    except json.JSONDecodeError as e:
        st.error(f"JSON Error: {e}")
        st.write(f"Raw Response: {result_str}")
    except (ValueError, Exception) as e:
        st.error(f"Error: {e}")

if __name__ == "__main__":
    main()