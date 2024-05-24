from config.model_config import *
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer(embedding_model_dict[selected_embedding_model])


def calculate_embedding(sentences):
    return embedding_model.encode(sentences)
