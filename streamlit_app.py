import os
import json
import requests
from dotenv import load_dotenv
from src.utils import validate_inputs
from src.prompt import mcq_prompt_template

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

class MCQGenerator:
    def __init__(self):
        self.api_url = "https://api.mistral.ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def generate_mcqs(self, input_text, num_questions, num_options, difficulty):
        validate_inputs(input_text, num_questions, num_options, difficulty)

        prompt = mcq_prompt_template.format(
            input_text=input_text,
            num_questions=num_questions,
            num_options=num_options,
            difficulty=difficulty
        )

        payload = {
            "model": "mistral-medium",  # or "mistral-tiny", "mistral-small"
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)

        if response.status_code != 200:
            raise ValueError(f"API Error: {response.status_code} - {response.text}")

        content = response.json()["choices"][0]["message"]["content"]

        try:
            mcqs = json.loads(content)
            return json.dumps(mcqs)
        except json.JSONDecodeError:
            start_index = content.find('[')
            end_index = content.rfind(']')
            if start_index != -1 and end_index != -1 and start_index < end_index:
                json_like_str = content[start_index:end_index + 1]
                try:
                    mcqs = json.loads(json_like_str)
                    return json.dumps(mcqs)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Failed to parse generated MCQs as JSON: {e} - Raw Response: {content}")
            else:
                raise ValueError(f"Failed to find JSON structure in generated MCQs. Raw Response: {content}")

if __name__ == "__main__":
    generator = MCQGenerator()
    result = generator.generate_mcqs("Python Programming", 2, 4, "easy")
    print(result)
