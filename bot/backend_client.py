import requests
from config import BACKEND_URL

def decode_message(boc: str):
    response = requests.post(f"{BACKEND_URL}/decode", json={"boc": boc})
    return response.json()

def emulate_events(boc: str):
    response = requests.post(f"{BACKEND_URL}/events", json={"boc": boc})
    return response.json()

def emulate_trace(boc: str):
    response = requests.post(f"{BACKEND_URL}/trace", json={"boc": boc})
    return response.json()

def emulate_wallet(boc: str, address: str, balance: int):
    data = {
        "boc": boc,
        "params": [
            {"address": address, "balance": balance}
        ]
    }
    response = requests.post(f"{BACKEND_URL}/wallet", json=data)
    return response.json()

def estimate_fees(hex_boc: str):
    url = f"{BACKEND_URL}/trace"
    response = requests.post(url, json={"boc": hex_boc})
    return response.json()
