from core.gemini_client import ask_gemini

def generate_quiz(text):
    prompt = f"""
    Create 10 multiple choice questions.

    Format:

    Question:
    A)
    B)
    C)
    D)

    Correct Answer:

    Notes:
    {text}
    """

    return ask_gemini(prompt)