import os, requests
from ...typing import sha256, Dict, get_type_hints
import json

url = "https://gpt4.xunika.uk/api/openai/v1/chat/completions"
model = ['gpt-3.5-turbo']
supports_stream = False
needs_auth = False

def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    base = ''
    for message in messages:
        base += '%s: %s\n' % (message['role'], message['content'])
    base += 'assistant:'
    
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }
    data = {
        "messages": [
            {
                "role": "system",
                "content": "You are ChatGPT, a large language model trained by OpenAI.\nKnowledge cutoff: 2021-09\nCurrent model: gpt-3.5-turbo-16k\nCurrent time: 7/5/2023, 4:26:40 PM\n"
            },
            {
                "role": "user",
                "content": "test"
            },
            {
                "role": "assistant",
                "content": "Hello! How can I assist you today?"
            },
            {
                "role": "user",
                "content": base
            }
        ],
        "stream": False,
        "model": "gpt-3.5-turbo",
        "temperature": 0.1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "top_p": 1
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response = response.json()
        yield response['choices'][0]['message']['content']
    else:
        print(f"Error Occurred::{response.status_code}")
        return None

params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])