import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

print("Listing models...")
try:
    for m in client.models.list():
        print(f"Model ID: {m.name}")
except Exception as e:
    print(f"Error: {e}")
