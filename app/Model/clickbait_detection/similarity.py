from sentence_transformers import SentenceTransformer,util

bert_model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_similarity(title:str, content:str) -> float:
    embedding = bert_model.encode([title,content], convert_to_tensor=True)
    sim_score = util.cos_sim(embedding[0], embedding[1]).item()
    return sim_score









