# 🧪 TON Emulator Bot

A developer-first **Telegram bot** paired with a lightweight **Flask backend** to help you:

* 🔍 Decode TON messages
* 🧠 Emulate execution in the TON VM
* 📅 Simulate on-chain events
* 👛 Test how messages affect wallet state
* ⛽ Estimate transaction fees

It's all powered by [TONAPI](https://tonapi.io/), giving developers a safe space to debug and simulate transactions **without ever touching the chain**.

---

## 📁 Project Structure

```
ton_emulator_project/
├── bot/                # Telegram bot (pyTelegramBotAPI)
├── backend/            # Flask backend that interacts with TONAPI
├── logs/               # Auto-generated log files
├── .env                # API tokens and config
├── run.sh              # Launch script for both bot and backend
├── requirements.txt    # Combined dependencies
└── README.md
```

---

## ⚙️ Features

| Command                      | What it does                                        |
| ---------------------------- | --------------------------------------------------- |
| `/decode <BOC>`              | Decodes a base64/hex-encoded BOC into readable JSON |
| `/trace <BOC>`               | Runs a VM trace on the message                      |
| `/events <BOC>`              | Simulates any events the message would emit         |
| `/wallet <BOC> <ADDR> <BAL>` | Emulates how the message would affect a wallet      |
| `/fees <BOC>`                | Estimates gas usage and TON fees                    |
| Inline buttons               | Quick access to Trace, Events, and Fees             |
| Logging + restart            | Crashes are logged and restarted automatically      |

---

## 🛰️ How This Uses TONAPI

This bot is essentially a UI for [TONAPI](https://tonapi.io)’s simulation endpoints — every command routes to a specific TONAPI endpoint that lets you test things without needing a real transaction or node setup.

| Command   | TONAPI Endpoint                              | Purpose                               |
| --------- | -------------------------------------------- | ------------------------------------- |
| `/decode` | `POST /v2/blockchain/message/decode`         | See what’s inside any BOC message     |
| `/trace`  | `POST /v2/blockchain/message/trace`          | Full VM trace, step-by-step           |
| `/events` | `POST /v2/blockchain/message/events`         | Preview events the message would emit |
| `/wallet` | `POST /v2/blockchain/message/wallet-emulate` | Emulates wallet state changes         |
| `/fees`   | `POST /v2/blockchain/message/estimate-fee`   | Get fee + gas estimates               |

Useful for dApp developers, contract authors, and explorers who want to test logic without risk.

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/ton-emulator-bot.git
cd ton-emulator-bot
```

---

### 2. Install dependencies

```bash
# Optional: create a venv
pip install -r requirements.txt
```

---

### 3. Set up environment variables

Create a `.env` file:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TON_API_TOKEN=your_tonapi_token_here
BACKEND_URL=http://localhost:8000
```

---

### 4. Run the project

```bash
chmod +x run.sh
./run.sh
```

Both the backend and bot will run in the background. Logs will go to:

```
logs/backend.log
logs/bot.log
```

---

## 💬 Example Commands (Telegram)

```
/start
/decode te6ccgEBA...
/trace te6ccgEBA...
/wallet te6ccgEBA... 0:abc123... 1000000000
```

You’ll get JSON results and quick buttons to continue inspecting each message.

---

## 📦 Deployment Notes

* The backend runs on **Gunicorn**
* The bot uses **infinite polling**
* You can deploy using:

  * Docker
  * supervisord
  * systemd
  * or just keep using `run.sh`

---

## 📜 Logs

Logs are saved in the `logs/` directory:

* `bot.log` – Telegram bot activity
* `backend.log` – Flask + Gunicorn output

---

## 🤝 Contributing

Open to pull requests — especially for bug fixes or new ideas. Just:

1. Fork the repo
2. Create a new branch
3. Submit a PR

---

## 📄 License

MIT License

---

## 🧾 Credits

* [TONAPI](https://tonapi.io) — simulation endpoints
* [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
* [Gunicorn](https://gunicorn.org)