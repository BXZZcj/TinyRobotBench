import uvicorn
import json
import datetime
from PIL import Image
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import LlavaForConditionalGeneration, AutoModelForCausalLM,AutoTokenizer, AutoProcessor
from config.model_config import *
from config.network_config import *
from typing import List, Tuple
import io
import base64
import sys


DEVICE = "cuda"
DEVICE_ID = "0"
CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}" if DEVICE_ID else DEVICE


def torch_gc():
    if torch.cuda.is_available():
        with torch.cuda.device(CUDA_DEVICE):
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/_stcore/health")
async def health_check():
    return {"message": "healthy"}


@app.get("/_stcore/allowed-message-origins")
async def allowed_message_origins_check():
    return {"message": "allowed"}


@app.post("/")
async def create_item(request: Request):
    global model, tokenizer
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw)
    json_post_list = json.loads(json_post)

    query = json_post_list.get('query')
    images_str = json_post_list.get('images_str')
    history = json_post_list.get('history')
    max_length = json_post_list.get('max_length')
    top_k = json_post_list.get('top_k')
    temperature = json_post_list.get('temperature')    
    print(query)

    images=None
    if images_str:
        # 解码图像数据
        images_bytes = base64.b64decode(images_str.encode('utf-8'))
        images = Image.open(io.BytesIO(images_bytes))
    else:
        images = Image.new('RGB', (14, 14), color = 'white')
        # pass

    response, history = chat_with_history(query=query,
                                          images=images,
                                          history=history,
                                          max_length=max_length if max_length else 2048,
                                          top_k=top_k if top_k else 50,
                                          # top_k=top_k if top_k else 1,
                                          do_sample=True,
                                          temperature=temperature if temperature else 1e-8)
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    answer = {
        "response": response,
        "history": history,
        "status": 200,
        "time": time
    }
    log = "[" + time + "] " + '", query:"' + query + '", response:"' + repr(response) + '"'
    print(log)
    torch_gc()
    return answer


@torch.inference_mode()
def chat_with_history(query: str, images:Image.Image, history: List[Tuple[str, str]] = None, **gen_kwargs):
    """
    带有历史信息的对话.
    :param query: 用户输入的对话语句.
    :param history: 历史对话信息, (query, response)组成的List.
    :param gen_kwargs: 生成参数, 参考https://huggingface.co/docs/transformers/v4.33.2/en/main_classes/text_generation#transformers.GenerationConfig.
    :return: response: str, history: List[Tuple[str, str]]
    """
    global model, processor
    if history is None:
        history = []
    prompt = "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, " \
             "detailed, and polite answers to the user's questions.\n\n"
    for (old_query, response) in history:
        prompt += f"USER: {old_query}\nASSISTANT: {response}</s>\n"
    prompt += f"USER: <image>\n{query}\nASSISTANT: "

    inputs = processor(text=prompt, images=images, return_tensors="pt")
    generate_ids = model.generate(**inputs, **gen_kwargs)
    answer=processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    
    history = history + [(query, answer)]
    return answer, history


if __name__ == '__main__':
    if len(sys.argv)>1:
        llm_name=sys.argv[1]
    else:
        print("please add the llm name as an argument! For example: python path_to_server_img.py llava-v1.6-vicuna-7b")
        sys.exit()

    model_path = llm_model_dict[llm_name]['local_model_path']
    model = LlavaForConditionalGeneration.from_pretrained(model_path)
    processor = AutoProcessor.from_pretrained(model_path)
    uvicorn.run(app, host='0.0.0.0', port=model_port, workers=1)
    