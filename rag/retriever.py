import numpy as np

def retrieve(query, model, index, chunks, k=3):
    query_vec = model.encode([query])

    distances, indices = index.search(np.array(query_vec), k)

    return [chunks[i] for i in indices[0]]