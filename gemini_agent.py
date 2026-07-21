import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ask_gemini(question, board_data):

    prompt = f"""
You are an expert Business Intelligence Assistant.

Business Data:
{board_data}

Question:
{question}

Answer only from the provided data.
Give concise business insights.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )
        return response.text

    except Exception:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        return response.text