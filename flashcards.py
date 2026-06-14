from core.gemini_client import ask_gemini

def generate_flashcards(text):
    prompt = f"""
    Create flashcards from these notes.

    Format:

    Q: ...
    A: ...

    Notes:
    {text}
    """

    return ask_gemini(prompt)