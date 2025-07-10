from langchain.prompts import PromptTemplate

mcq_prompt_template = PromptTemplate(
    input_variables=["input_text", "num_questions", "num_options", "difficulty"],
    template="""Generate {num_questions} multiple choice questions about the following topic/text: '{input_text}'.
    Each question should have {num_options} options. Indicate the correct answer clearly within the JSON format.
    If the difficulty is 'Mixed', generate a random mix of Easy, Medium, and Hard questions. If specific counts 
    are provided (e.g., Easy:2, Medium:3), generate that many questions per level. Use the counts from: {difficulty}."

    Format the output as a JSON array of dictionaries, where each dictionary represents a question and has the following keys:
    "question": the question text,
    "options": a list of strings representing the options,
    "correct_answer": the correct answer from the options.
    """,
)