from langchain_mistralai.chat_models import ChatMistralAI
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
import json
from srcm.utils import validate_inputs
from srcm.prompt import mcq_prompt_template

load_dotenv()
api_token = os.getenv("MISTRAL_API_KEY")

llm = ChatMistralAI(
    model="mistral-medium",
    mistral_api_key=api_token,
    temperature=0.7,
    max_tokens=1000
)

class MCQGenerator:
    def generate_mcqs(self, input_text, num_questions, num_options, difficulty):
        validate_inputs(input_text, num_questions, num_options, difficulty)
        if isinstance(difficulty, list):
            difficulty_text = ", ".join(difficulty)
        else:
            difficulty_text = difficulty

        if isinstance(difficulty, dict):
            difficulty_text = ", ".join(
                f"{level.capitalize()}:{count}" for level, count in difficulty.items() if count > 0
                )
        elif isinstance(difficulty, str) and difficulty.lower() == "mixed":
            difficulty_text = "Mixed"
        else:difficulty_text = str(difficulty)

        prompt = mcq_prompt_template.format(
            input_text=input_text,
            num_questions=num_questions,
            num_options=num_options,
            difficulty=difficulty_text
            )


        response = llm.invoke(prompt) 
        response_text = ""
        if isinstance(response, str):
            response_text = response
        elif hasattr(response, 'content'):
            response_text = response.content
        else:
            raise ValueError(f"Unexpected response type from LLM: {type(response)}")
        
        try:
            mcqs = json.loads(response_text)
            return json.dumps(mcqs)
        except json.JSONDecodeError:
            start_index = response_text.find('[')
            end_index = response_text.rfind(']')
        if start_index != -1 and end_index != -1 and start_index < end_index:
            json_like_str = response_text[start_index:end_index + 1]
            try:
                mcqs = json.loads(json_like_str)
                return json.dumps(mcqs)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse generated MCQs as JSON: {e} - Raw Response: {response_text}")
        else:
            raise ValueError(f"Failed to find JSON structure in generated MCQs. Raw Response: {response_text}")