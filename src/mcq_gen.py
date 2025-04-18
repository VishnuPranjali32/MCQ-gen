from langchain.llms import HuggingFaceHub
from dotenv import load_dotenv
import os
from src.utils import validate_inputs
from src.prompt import mcq_prompt_template

# Load API token from .env
load_dotenv()
api_token = os.getenv("HUGGINGFACE_API_TOKEN")

# Initialize the model
llm = HuggingFaceHub(
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    huggingfacehub_api_token=api_token,
    model_kwargs={"temperature": 0.7, "max_length": 500}
)

def generate_mcq(input_text, num_questions, num_options, difficulty):
    # Validate inputs
    validate_inputs(input_text, num_questions, num_options, difficulty)

    # Format the prompt
    prompt = mcq_prompt_template.format(
        input_text=input_text,
        num_questions=num_questions,
        num_options=num_options,
        difficulty=difficulty
    )

    # Generate response
    response = llm(prompt)
    return response

if __name__ == "__main__":
    # Example usage
    result = generate_mcq("Python Programming", 2, 4, "easy")
    print(result)