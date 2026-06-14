from core.gemini_client import ask_gemini

def summarize_notes(text):
    prompt = f"""
    Summarize the following notes.

    Give:
    1. Main topics
    2. Key concepts
    3. Important points
    4. Short revision notes

    Notes:
    {text}
    """

    return ask_gemini(prompt)