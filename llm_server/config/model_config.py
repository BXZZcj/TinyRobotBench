import os
import logging
import torch
# 日志格式
LOG_FORMAT = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(format=LOG_FORMAT)


embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "text2vec-base": "shibing624/text2vec-base-chinese",
    "text2vec": "GanymedeNil/text2vec-large-chinese",
    "text2vec-paraphrase": "shibing624/text2vec-base-chinese-paraphrase",
    "text2vec-sentence": "shibing624/text2vec-base-chinese-sentence",
    "text2vec-multilingual": "shibing624/text2vec-base-multilingual",
    "m3e-small": "moka-ai/m3e-small",
    "m3e-base": "m3e-base",
    "m3e-large": "moka-ai/m3e-large",
    "bge-small-zh": "BAAI/bge-small-zh",
    "bge-base-zh": "BAAI/bge-base-zh",
    "bge-large-zh": "BAAI/bge-large-zh",
    "bge-large-zh-noinstruct": "BAAI/bge-large-zh-noinstruct",
    "text-embedding-ada-002": os.environ.get("OPENAI_API_KEY")
}


llm_model_dict = {
    "chatglm2-6b": {
        "local_model_path": "/workspace/2023/chatglm2-6b"
    },

    "vicuna-13b-v1.5-GPTQ": {
        "local_model_path": "vicuna-13B-v1.5-GPTQ"
    },

    "llava-v1.6-vicuna-7b": {
        "local_model_path": "llava-v1.6-vicuna-7b"
    },
    
    "gpt-3.5-turbo": {
        "local_model_path": "gpt-3.5-turbo"
    },
}
