import requests
import os
import json

PRIMARY_MEMORY_ENDPOINT = os.getenv("MIND_BANK_PRIMARY", "http://gpt-memory.internal")
FALLBACK_GITHUB_RAW = os.getenv("MIND_BANK_FALLBACK", "https://raw.githubusercontent.com/collierjc75/MindBank/main/mindbank")

def is_memory_online():
    try:
        response = requests.get(f"{PRIMARY_MEMORY_ENDPOINT}/ping", timeout=2)
        return response.status_code == 200
    except requests.RequestException:
        return False

def resolve(uri):
    if not uri.startswith("mindbank://"):
        raise ValueError("Invalid URI format")
    path = uri.replace("mindbank://", "").strip("/")
    if is_memory_online():
        try:
            response = requests.get(f"{PRIMARY_MEMORY_ENDPOINT}/{path}")
            response.raise_for_status()
            return response.json()
        except:
            pass
    fallback_url = f"{FALLBACK_GITHUB_RAW}/{path}"
    response = requests.get(fallback_url)
    response.raise_for_status()
    return response.json()

def get_summary(uri):
    summary_uri = uri.replace(".json", "_summary.txt")
    if is_memory_online():
        try:
            response = requests.get(f"{PRIMARY_MEMORY_ENDPOINT}/{summary_uri}")
            if response.ok:
                return response.text
        except:
            pass
    fallback_url = f"{FALLBACK_GITHUB_RAW}/{summary_uri}"
    response = requests.get(fallback_url)
    if response.ok:
        return response.text
    return "Summary not available."

def cache(uri, payload):
    cache_dir = "/tmp/mindbank_cache"
    os.makedirs(cache_dir, exist_ok=True)
    file_path = os.path.join(cache_dir, uri.replace("mindbank://", "").replace("/", "_"))
    with open(file_path, "w") as f:
        json.dump(payload, f)
