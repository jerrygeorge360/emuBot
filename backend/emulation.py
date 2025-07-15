import os
import requests
from dotenv import load_dotenv

load_dotenv()

TON_API_TOKEN = os.getenv('TON_API_TOKEN')
BASE_URL = "https://tonapi.io"
HEADERS = {
    "Authorization": f"Bearer {TON_API_TOKEN}",
    "Content-Type": "application/json"
}

def emulation_decode(boc: str):
    url = f"{BASE_URL}/v2/message/decode"
    resp = requests.post(url, json={"boc": boc}, headers=HEADERS)
    return safe_json(resp)

def emulate_message_events(boc: str):
    url = f"{BASE_URL}/v2/events/emulate"
    params = {"ignore_signature_check": "true"}
    resp = requests.post(url, json={"boc": boc}, headers=HEADERS, params=params)
    return safe_json(resp)

def emulate_message_trace(boc: str):
    url = f"{BASE_URL}/v2/traces/emulate"
    params = {"ignore_signature_check": "true"}
    resp = requests.post(url, json={"boc": boc}, headers=HEADERS, params=params)
    return safe_json(resp)

def emulate_wallet_message(boc: str, params: list):
    url = f"{BASE_URL}/v2/wallet/emulate"
    resp = requests.post(url, json={"boc": boc, "params": params}, headers=HEADERS)
    return safe_json(resp)

def safe_json(resp):
    try:
        return resp.json()
    except ValueError:
        return {"error": "Invalid JSON", "status": resp.status_code, "raw": resp.text}
