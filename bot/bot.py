import telebot
from telebot import types
from bot.config import BOT_TOKEN
from bot.demo import demo_boc_value
from bot.backend_client import (
    decode_message,
    emulate_events,
    emulate_trace,
    emulate_wallet,
    estimate_fees,
)

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

# start & help
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Decode", callback_data="demo_decode"),
        types.InlineKeyboardButton("Trace", callback_data="demo_trace"),
    )
    markup.add(
        types.InlineKeyboardButton("Events", callback_data="demo_events"),
        types.InlineKeyboardButton("Estimate Fees", callback_data="demo_fees")
    )

    bot.send_message(
        message.chat.id,
        "👋 *Welcome to TON Emulator Bot!*\n\n"
        "Emulate and inspect TON blockchain messages safely.\n\n"
        "*Commands:*\n"
        "`/decode <boc>` – Decode message\n"
        "`/events <boc>` – Simulate events\n"
        "`/trace <boc>` – VM trace\n"
        "`/wallet <boc> <address> <balance>` – Simulate wallet result\n"
        "`/fees <boc>` – Gas & fee estimate\n\n"
        "👇 Try a sample action:",
        reply_markup=markup
    )

# Callback demo buttons
@bot.callback_query_handler(func=lambda call: call.data.startswith("demo_"))
def handle_demo_callback(call):
    demo_boc = demo_boc_value
    if call.data == "demo_decode":
        result = decode_message(demo_boc)
        text = f"🧠 *Decoded Message Sample*\n`{result}`"
    elif call.data == "demo_trace":
        result = emulate_trace(demo_boc)
        text = f"🔍 *VM Trace Sample*\n`{result}`"
    elif call.data == "demo_events":
        result = emulate_events(demo_boc)
        text = f"📢 *Event Result Sample*\n`{result}`"
    elif call.data == "demo_fees":
        result = estimate_fees(demo_boc)
        compute = result.get("compute", {})
        gas = compute.get("gas_used", "N/A")
        ton = float(gas) * 0.05 / 1e9 if isinstance(gas, int) else "N/A"
        text = f"💸 *Sample Fee Estimate*\nGas: `{gas}`\nTON: `{ton}`"
    else:
        text = "❓ Unknown demo"
    bot.send_message(call.message.chat.id, text)

# decode
@bot.message_handler(commands=["decode"])
def handle_decode(message):
    try:
        _, boc = message.text.split(" ", 1)
        result = decode_message(boc.strip())
        msg = bot.reply_to(message, f"🧠 *Decoded:*\n```{result}```")
        add_action_buttons(msg, boc.strip())
    except Exception as e:
        bot.reply_to(message, f"❌ Error:\n{e}")

# events
@bot.message_handler(commands=["events"])
def handle_events(message):
    try:
        _, boc = message.text.split(" ", 1)
        result = emulate_events(boc.strip())
        bot.reply_to(message, f"📢 *Events:*\n```{result}```")
    except Exception as e:
        bot.reply_to(message, f"❌ Error:\n{e}")

# trace
@bot.message_handler(commands=["trace"])
def handle_trace(message):
    try:
        _, boc = message.text.split(" ", 1)
        result = emulate_trace(boc.strip())
        bot.reply_to(message, f"🔍 *Trace:*\n```{result}```")
    except Exception as e:
        bot.reply_to(message, f"❌ Error:\n{e}")

# wallet
@bot.message_handler(commands=["wallet"])
def handle_wallet(message):
    try:
        _, boc, address, balance = message.text.split(" ", 3)
        result = emulate_wallet(boc.strip(), address.strip(), int(balance.strip()))
        bot.reply_to(message, f"💼 *Wallet Result:*\n```{result}```")
    except Exception as e:
        bot.reply_to(message, f"❌ Error:\n{e}")

# fees
@bot.message_handler(commands=["fees"])
def handle_fees(message):
    try:
        _, boc = message.text.split(" ", 1)
        result = estimate_fees(boc.strip())
        compute = result.get("compute", {})
        gas = compute.get("gas_used", "N/A")
        ton = float(gas) * 0.05 / 1e9 if isinstance(gas, int) else "N/A"
        text = (
            f"💸 *Fee Estimate*\n"
            f"Gas Used: `{gas}`\n"
            f"TON Est.: `{ton}`"
        )
        msg = bot.reply_to(message, text)
        add_action_buttons(msg, boc.strip())
    except Exception as e:
        bot.reply_to(message, f"❌ Error:\n{e}")

# action inline buttons
def add_action_buttons(message, boc: str):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📢 Events", callback_data=f"act_events|{boc}"),
        types.InlineKeyboardButton("🔍 Trace", callback_data=f"act_trace|{boc}"),
        types.InlineKeyboardButton("💸 Fees", callback_data=f"act_fees|{boc}")
    )
    bot.edit_message_reply_markup(message.chat.id, message.message_id, reply_markup=markup)

# button actions
@bot.callback_query_handler(func=lambda call: call.data.startswith("act_"))
def handle_action_callback(call):
    action, boc = call.data.split("|", 1)
    try:
        if action == "act_events":
            result = emulate_events(boc)
            text = f"📢 *Events:*\n```{result}```"
        elif action == "act_trace":
            result = emulate_trace(boc)
            text = f"🔍 *Trace:*\n```{result}```"
        elif action == "act_fees":
            result = estimate_fees(boc)
            gas = result.get("compute", {}).get("gas_used", "N/A")
            ton = float(gas) * 0.05 / 1e9 if isinstance(gas, int) else "N/A"
            text = f"💸 *Gas:* `{gas}`\n*TON:* `{ton}`"
        else:
            text = "❓ Unknown action"
        bot.send_message(call.message.chat.id, text)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ Error:\n{e}")

if __name__ == "__main__":
    print("Bot running")
    bot.infinity_polling()
