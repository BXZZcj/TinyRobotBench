import requests
import json
import argparse
import base64
import subprocess


parser = argparse.ArgumentParser(description="Send POST request with parameters")
parser.add_argument('query', type=str, help='The prompt for LLM')
parser.add_argument('--image_path', default=None, type=str, help='Path to the image file')
parser.add_argument("--top_k", default=10, type=int, help="Top K predictions to consider (default: 10)")
parser.add_argument("--max_length", default=2048, type=int, help="Maximum length of the response (default: 100)")
parser.add_argument("--temperature", default=0.7, type=float, help="Temperature for sampling (default: 0.7)")


args = parser.parse_args()

image_path=args.image_path
if image_path!=None:
    with open(args.image_path, "rb") as img_file:
        image_data = base64.b64encode(img_file.read()).decode('utf-8')
else:
    image_data=None


url = "https://u102232-8229-b10afc7e.westb.seetacloud.com:8443/"

data = {
    "query": args.query,
    "history": [],  
    "images_str": image_data,
    "top_k": args.top_k,
    "max_length": args.max_length,
    "temperature": args.temperature
}

json_data = json.dumps(data)

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, data=json_data)

if response.status_code == 200:
    print("Request successful!")
    llm_generated_func  = json.loads(response.text)["response"]
    print("Response:\n", llm_generated_func )
else:
    print("Request failed with status code:", response.status_code)

# llm_generated_func = \
# """def plan():
#     box_position = get_box_position()
#     object_names = get_names_on_table()
#     for name in object_names:
#         object_position = get_location_by_name(name)
#         move_tool(object_position)
#         grasp()
#         move_tool(box_position)
#         ungrasp()"""

execute="./manipulate/tasks/exec_llm_code.py"
subprocess.run(['python', execute, llm_generated_func])
