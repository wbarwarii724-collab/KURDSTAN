# -*- coding: utf-8 -*-
import asyncio
import random
from telegram import Bot
from telegram.error import TelegramError

# ===== CONFIG =====
BOT_TOKEN = "8839560847:AAF3IeRKYVerZUUHYV_ZgfItdm4BPEhcBYk"
CHANNEL_ID = "@CC428Kurd"
ADMIN_ID = 6395195181
CARD_DATA = {
    "number": "4095131982174501",
    "month": "07",
    "year": "2035",
    "cvv": "580"
}
INTERVAL_SECONDS = 2
# ==============================================

async def send_card_message(bot, channel, admin):
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
        # ناردنی پەیام بۆ کەناڵ
        mmsg = await bot.send_message(chat_id=channel, text=text)
        # ناردنی پەیامی سەرکەوتن بۆ ئەدمین
        await bot.send_message(chat_id=admin, text=f"[SUCCESS] Sent to {channel}\nMsg ID: {mmsg.message_id}")
        return True
    except TelegramError as e:
        await bot.send_message(chat_id=admin, text=f"[ERROR] {str(e)}")
        return False

async def main():
    bot = Bot(token=BOT_TOKEN)
    try:
        bot.get_me()
    except TelegramError:
        print("Error: invalid token or no internet.")
        return

    while True:
        success = await send_card_message(bot, CHANNEL_ID, ADMIN_ID)
        delay = INTERVAL_SECONDS * random.uniform(0.9, 1.1)
        await asyncio.sleep(delay)

if __name__ == "__main__":
    asyncio.run(main())
