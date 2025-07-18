# TON Emulator Bot

A developer-friendly **Telegram bot** with a connected **Flask backend**, allowing you to:

* Decode TON messages
* Emulate message execution
* Trigger event simulation
* Simulate wallet state
* Estimate transaction fees

Everything is powered by the [TONAPI](https://tonapi.io/) and designed to help developers test and inspect messages **without broadcasting them**.

---

## 📁 Project Structure

```
ton_emulator_project/
├── bot/                # Telegram bot (pyTelegramBotAPI)
│   ├── bot.py
│   ├── backend_client.py
│   └── config.py
├── backend/            # Flask backend calling TONAPI
│   ├── app.py
│   ├── emulation.py
│   └── config.py
├── logs/               # Auto-generated log files
├── .env                # API tokens and secrets
├── run.sh              # Starts both bot + backend with logging and restart
├── requirements.txt    # Combined requirements
└── README.md
```

---

## ⚙️ Features

| Feature                      | Description                                      |
| ---------------------------- | ------------------------------------------------ |
| `/decode <BOC>`              | Decodes a base64 or hex BOC message              |
| `/trace <BOC>`               | Returns VM execution trace                       |
| `/events <BOC>`              | Simulates on-chain events triggered by message   |
| `/wallet <BOC> <ADDR> <BAL>` | Simulates message impact on wallet state         |
| `/fees <BOC>`                | Estimates gas used and equivalent TON cost       |
| Inline buttons               | Quick actions like “Trace”, “Events”, “Fees”     |
| Logs + Monitoring            | Crashes are auto-restarted, logs written to disk |

---

## 🧪 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/ton-emulator-bot.git
cd ton-emulator-bot
```

---

### 2. Install dependencies

```bash
# (Optionally create a virtual environment)
pip install -r requirements.txt
```

---

### 3. Set up `.env`

Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TON_API_TOKEN=your_tonapi_token_here
BACKEND_URL=http://localhost:8000
```

---

### 4. Run the project

Use the built-in `run.sh` script to launch both services:

```bash
chmod +x run.sh
./run.sh
```

Logs will be saved in the `logs/` folder.

---

## 🧠 Example Usage (Telegram)

```text
/start
/decode te6ccgEBA...
/trace te6ccgEBA...
/wallet te6ccgEBA... 0:abc... 1000000000
```

You’ll receive nicely formatted JSON and inline buttons to continue exploring each message.

---

## 📦 Deployment Notes

* Flask backend is served via **Gunicorn**
* Bot runs using **infinite polling**
* You can deploy using **Docker**, **supervisord**, or **systemd** (your choice)

---

## 📜 Logs

Logs are stored in:

```
logs/bot.log
logs/backend.log
```

---

## 🤝 Contributing

Contributions are welcome! To propose a fix or feature:

1. Fork the repo
2. Create a new branch
3. Submit a pull request

---

## 📄 License

MIT License

---

## 🧾 Credits

* [TONAPI.io](https://tonapi.io) — The TON blockchain API
* [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
* [Gunicorn](https://gunicorn.org) — Python WSGI HTTP Server

---