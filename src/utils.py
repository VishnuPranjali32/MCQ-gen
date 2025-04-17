import re

def clean_text(text: str) -> str:
    """Clean input text by removing extra whitespace and special characters."""
    text = re.sub(r'\s+', ' ', text.strip())
    return text

def validate_inputs(
    input_text: str, num_questions: int, num_options: int, difficulty: str
) -> None:
    """Validate user inputs."""
    if not input_text:
        raise ValueError("Input text or topic cannot be empty.")
    if num_questions < 1:
        raise ValueError("Number of questions must be at least 1.")
    if num_options < 2:
        raise ValueError("Number of options must be at least 2.")
    if difficulty.lower() not in ["easy", "medium", "hard"]:
        raise ValueError("Difficulty must be 'easy', 'medium', or 'hard'.")