from langchain.prompts import PromptTemplate

mcq_prompt_template = PromptTemplate(
    input_variables=["input_text", "num_questions", "num_options", "difficulty"],
    template="""Generate {num_questions} multiple choice questions about the following topic/text: '{input_text}'.
    Each question should have {num_options} options. Indicate the correct answer clearly within the JSON format.
    The difficulty level of the questions should be {difficulty}.

    Format the output as a JSON array of dictionaries, where each dictionary represents a question and has the following keys:
    "question": the question text,
    "options": a list of strings representing the options,
    "correct_answer": the correct answer from the options.
    """,
)