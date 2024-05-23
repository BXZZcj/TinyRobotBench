from config.model_config import *
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer(embedding_model_dict['m3e-base'])


def calculate_embedding(sentences):
    return embedding_model.encode(sentences)
