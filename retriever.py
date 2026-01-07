import torch
from sentence_transformers import util

class Retriever:
    def __init__(self, embeddings, chunks):
        self.embeddings = embeddings
        self.chunks = chunks

    def retrieve(self, query_embedding, top_k=8):
        scores = util.cos_sim(query_embedding, self.embeddings)[0]

        # ✅ FIX: prevent top_k overflow
        k = min(top_k, len(self.chunks))

        top_results = torch.topk(scores, k=k)

        results = []
        for idx in top_results.indices:
            results.append(self.chunks[idx])

        return results
