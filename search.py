from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def search(query_embedding, index, top_k=5, threshold=0.35):

    vectors = [item["embedding"] for item in index]
    paths = [item["path"] for item in index]

    sims = cosine_similarity([query_embedding], vectors)[0]

    ranked = np.argsort(sims)[::-1]

    results = []
    for i in ranked:
        if sims[i] < threshold:
            continue
        results.append((paths[i], sims[i]))
        if len(results) >= top_k:
            break

    return results