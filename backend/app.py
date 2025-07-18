from flask import Flask, request, jsonify
from backend.emulation import (
    emulation_decode,
    emulate_message_events,
    emulate_message_trace,
    emulate_wallet_message,
)

app = Flask(__name__)

@app.route("/decode", methods=["POST"])
def decode():
    data = request.json
    boc = data.get("boc")
    if not boc:
        return jsonify({"error": "Missing BOC"}), 400
    result = emulation_decode(boc)
    return jsonify(result)

@app.route("/events", methods=["POST"])
def events():
    data = request.json
    boc = data.get("boc")
    if not boc:
        return jsonify({"error": "Missing BOC"}), 400
    result = emulate_message_events(boc)
    return jsonify(result)

@app.route("/trace", methods=["POST"])
def trace():
    data = request.json
    boc = data.get("boc")
    if not boc:
        return jsonify({"error": "Missing BOC"}), 400
    result = emulate_message_trace(boc)
    return jsonify(result)

@app.route("/wallet", methods=["POST"])
def wallet():
    data = request.json
    boc = data.get("boc")
    params = data.get("params", [])
    if not boc or not params:
        return jsonify({"error": "Missing BOC or params"}), 400
    result = emulate_wallet_message(boc, params)
    return jsonify(result)

@app.route("/")
def root():
    return "TON Emulation API is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
