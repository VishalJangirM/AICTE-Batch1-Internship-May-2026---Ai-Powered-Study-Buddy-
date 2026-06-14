import re

def chunk_text(text, chunk_size=500, overlap=100):
    if not text:
        return []

    text = " ".join(str(text).split())

    sentences = re.split(r'(?<=[.!?]) +', text)

    chunks = []
    current = []

    for sentence in sentences:
        current.append(sentence)

        if len(" ".join(current).split()) >= chunk_size:
            chunks.append(" ".join(current))
            current = current[-overlap:]  # keep overlap context

    if current:
        chunks.append(" ".join(current))

    return chunks