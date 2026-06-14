import faiss
import numpy as np

def build_index(embeddings):
    """Creates a new index from scratch."""
    if embeddings is None or len(embeddings) == 0:
        return None
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype('float32'))
    return index

def add_to_index(index, new_embeddings):
    """Adds new embeddings to an existing index."""
    if index is None:
        return build_index(new_embeddings)
    if new_embeddings is not None and len(new_embeddings) > 0:
        index.add(np.array(new_embeddings).astype('float32'))
    return index

def search_index(index, chunks, query, model, k=3):
    """Searches the index and returns relevant chunks."""
    if index is None or not chunks:
        return []
    
    query_vec = model.encode([query]).astype('float32')
    k = min(k, index.ntotal)
    if k == 0:
        return []
        
    distances, indices = index.search(query_vec, k)
    return [chunks[i] for i in indices[0] if i != -1]