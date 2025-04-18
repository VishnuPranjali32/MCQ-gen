from langchain.prompts import PromptTemplate

mcq_prompt_template = PromptTemplate(
    input_variables=["input_text", "num_questions", "num_options", "difficulty"],
    template="""
    Generate {num_questions} multiple-choice questions (MCQs) about the topic: "{input_text}".
    Each question should have {num_options} options, including one correct answer. Set difficulty to {difficulty}.
    Return the output as a JSON list of dictionaries, where each dictionary has keys: "question", "options" (list of strings), and "correct_answer" (string).
    """
)