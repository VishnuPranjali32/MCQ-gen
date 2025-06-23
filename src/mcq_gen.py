import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_community.llms import HuggingFaceHub
from dotenv import load_dotenv
import json
from src.utils import validate_inputs
from src.prompt import mcq_prompt_template

load_dotenv()
api_token = os.getenv("HUGGINGFACE_API_TOKEN")

llm = HuggingFaceHub(
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    huggingfacehub_api_token=api_token,
    model_kwargs={"temperature": 0.7, "max_length": 1000}
)

class MCQGenerator:
    def generate_mcqs(self, input_text, num_questions, num_options, difficulty):
        validate_inputs(input_text, num_questions, num_options, difficulty)
        prompt = mcq_prompt_template.format(
            input_text=input_text,
            num_questions=num_questions,
            num_options=num_options,
            difficulty=difficulty
        )
        response = llm(prompt)
        try:
            # Attempt to parse the response as JSON
            mcqs = json.loads(response)
            return json.dumps(mcqs)
        except json.JSONDecodeError:
            # Try to extract JSON-like part from raw text
            start_index = response.find('[')
            end_index = response.rfind(']')
            if start_index != -1 and end_index != -1 and start_index < end_index:
                json_like_str = response[start_index:end_index + 1]
                try:
                    mcqs = json.loads(json_like_str)
                    return json.dumps(mcqs)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Failed to parse generated MCQs as JSON: {e} - Raw Response: {response}")
            else:
                raise ValueError(f"Failed to find JSON structure in generated MCQs. Raw Response: {response}")

if __name__ == "__main__":
    generator = MCQGenerator()
    result = generator.generate_mcqs("Python Programming", 2, 4, "easy")
    print(result)
