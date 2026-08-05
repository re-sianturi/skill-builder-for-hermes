import os
import sys
import json
import urllib.request
import re

MODEL = "cf/@cf/meta/llama-3.3-70b-instruct-fp8-fast"
BASE_URL = "https://9router.gass.web.id/v1/chat/completions"
API_KEY = os.environ.get("NINE_ROUTER_API_KEY", "")

def call_llm(system_prompt, user_prompt, temperature=0.1):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature,
        "max_tokens": 3000
    }
    req = urllib.request.Request(
        BASE_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            if "data: [DONE]" in res_body:
                res_body = res_body.replace("data: [DONE]", "").strip()
            data = json.loads(res_body)
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error calling LLM in module: {e}", file=sys.stderr)
        raise e

def clean_json_string(text):
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        raw_json = match.group(0)
        try:
            json.loads(raw_json)
            return raw_json
        except json.JSONDecodeError as e:
            return raw_json[:e.pos]
    return text
