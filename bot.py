# -*- coding: utf-8 -*-
import asyncio
import random
from telegram import Bot
from telegram.error import TelegramError

# ===== CONFIG =====
BOT_TOKEN = "8839560847:AAF3IeRKYVerZUUHYV_ZgfItdm4BPEhcBYk"
CHANNEL_ID = "@CC428Kurd"
ADMIN_ID = 6395195181
INTERVAL_SECONDS = 2
# ==============================================

async def send_card_message(bot, channel, admin):
    # دروستکردنی کارتێکی نوێ بە ڕێکەوت (Random)
    card_number = f"4{random.randint(100000000000000, 999999999999999)}"
    month = str(random.randint(1, 12)).zfill(2)
    year = str(random.randint(2026, 2036))
    cvv = str(random.randint(100, 999))
    
    text = (f"💰 CARD DUMP\n"
            f"Card: {card_number}\n"
            f"Exp: {month}/{year}\n"
            f"CVV: {cvv}\n"
            f"Bank: ICICI BANK LTD\n"
            f"Country: INDIA\n"
            f"Type: VISA DEBIT PLATINUM\n"
            f"----\n"
            f"Scrapper: Hamody")
    
    try:
        mmsg = await bot.send_message(chat_id=channel, text=text)
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
        await send_card_message(bot, CHANNEL_ID, ADMIN_ID)
        delay = INTERVAL_SECONDS * random.uniform(0.9, 1.1)
        await asyncio.sleep(delay)

if __name__ == "__main__":
    asyncio.run(main())
