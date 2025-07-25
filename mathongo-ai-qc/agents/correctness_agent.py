import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

from utils import load_prompt
from response_cleaner import extract_clean_json


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

def correctness_agent(question_text: str) -> dict:
    prompt_template = load_prompt("correctness_prompt")
    prompt = prompt_template.format(question_text=question_text)

    model = genai.GenerativeModel(GEMINI_MODEL)
    generation_config = genai.types.GenerationConfig(
        temperature=0.7,
    )
    try:
        response = model.generate_content(prompt, generation_config=generation_config)
        print(f"[correctness_agent] Raw Gemini response: {response.text!r}")
        if not response.text or not response.text.strip():
            raise ValueError("Empty response from Gemini model.")
        try:
            feedback = extract_clean_json(response.text)
        except Exception as e:
            print("Error in correctness_agent:", e)
            return {
                "is_correct": False,
                "errors": ["LLM processing error or invalid JSON output.", str(e)],
                "explanation": f"An error occurred during AI processing: {e}"
            }
        return feedback
    except Exception as e:
        print(f"Error in correctness_agent: {e}")
        return {
            "is_correct": False,
            "errors": ["LLM processing error or invalid JSON output.", str(e)],
            "explanation": f"An error occurred during AI processing: {e}"
        }
