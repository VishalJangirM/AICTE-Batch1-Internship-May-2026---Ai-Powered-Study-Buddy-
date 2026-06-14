from core.gemini_client import ask_gemini


def answer_question(context, question):
    """
    Standard QA (fallback mode - full text or large context)
    """

    prompt = f"""
You are an expert AI tutor.

Your job is to answer questions ONLY using the study material provided.

RULES:
- If the answer is not in the material, say: "Not found in the provided material."
- Do NOT make up information.
- Keep answers simple, clear, and student-friendly.
- Use bullet points if helpful.

-------------------------
STUDY MATERIAL:
{context}
-------------------------

QUESTION:
{question}

ANSWER:
"""

    return ask_gemini(prompt)


def answer_question_rag(retrieved_chunks, question):
    """
    RAG mode (recommended for your upgraded system)
    Uses only relevant chunks retrieved from vector DB
    """

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are an intelligent AI tutor working with retrieved knowledge chunks.

STRICT RULES:
- Use ONLY the given context
- If answer is not present, say: "Not found in the provided context."
- Do not hallucinate or assume extra information
- Be concise and exam-friendly

-------------------------
RETRIEVED CONTEXT:
{context}
-------------------------

QUESTION:
{question}

Provide a clear answer:
"""

    return ask_gemini(prompt)