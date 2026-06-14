import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY missing in .env")

client = genai.Client(api_key=API_KEY)

MODEL = "models/gemini-2.5-flash"

def ask_gemini(prompt, retries=3):
    last_error = "Unknown error"
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config={
                    'safety_settings': [
                        {'category': 'HARM_CATEGORY_HATE_SPEECH', 'threshold': 'BLOCK_NONE'},
                        {'category': 'HARM_CATEGORY_HARASSMENT', 'threshold': 'BLOCK_NONE'},
                        {'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT', 'threshold': 'BLOCK_NONE'},
                        {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT', 'threshold': 'BLOCK_NONE'}
                    ]
                }
            )

            try:
                if response and response.text:
                    return response.text
                else:
                    return "Gemini returned an empty or blocked response. Try rephrasing your question."
            except ValueError:
                return "The response was blocked by Gemini's safety filters. Please try rephrasing."

        except Exception as e:
            last_error = str(e)
            if "429" in last_error or "quota" in last_error.lower():
                if attempt < retries - 1:
                    time.sleep(5)
                    continue
            
    return f"Gemini is currently unavailable. Error Summary: {last_error}"