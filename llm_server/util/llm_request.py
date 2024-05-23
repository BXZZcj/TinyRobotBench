import requests
import json
import argparse
from config.network_config import *


def request_llm(query, history=None, images_str=None, **gen_kwargs):
    base_url = f'http://127.0.0.1:{model_port}'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=base_url, headers=headers, json={"query": query, "history": history, "images_str":images_str, **gen_kwargs})
    result = json.loads(response.text)
    assert result['status'] == 200
    return result


def parse_args():
    parser = argparse.ArgumentParser(description='LLM Request Script')
    parser.add_argument('query', type=str, help='The query for LLM')
    parser.add_argument('--history', type=str, default=None, help='The history for LLM')
    parser.add_argument('--images_str', type=str, default=None, help='The images_str for LLM')
    parser.add_argument('--gen_kwargs', nargs='*', type=str, default=[], help='Additional keyword arguments for LLM as key=value pairs')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    response = request_llm(args.query, args.history, args.images_str, **dict(item.split('=') for item in args.gen_kwargs))
    print(response)
