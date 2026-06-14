from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

print("API key loaded:", bool(api_key))

client = genai.Client(api_key=api_key)

# List one model
for model in client.models.list():
    print("Found model:", model.name)
    break

# Test generation
response = client.models.generate_content(
    model="models/gemini-2.5-flash",
    contents="Say hello"
)

print(response.text)