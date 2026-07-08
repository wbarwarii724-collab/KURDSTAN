# -*- coding: utf-8 -*-
import asyncio
import os
from telegram import Bot
from telegram.error import TelegramError

# ===== CONFIG =====
BOT_TOKEN = "8839560847:AAF3IeRKYVerZUUHYV_ZgfItdm4BPEhcBYk"
CHANNEL_ID = "@CC428Kurd"
ADMIN_ID = 6395195181
INTERVAL_SECONDS = 2
# ==============================================

async def send_cards_text(bot, channel, admin):
    file_path = 'cards.txt'
    
    if not os.path.exists(file_path):
        await bot.send_message(chat_id=admin, text="[ERROR] cards.txt file not found!")
        return False

    try:
        # خوێندنەوەی هەموو کارتەکانی ناو فایلەکە
        with open(file_path, 'r', encoding='utf-8') as f:
            cards_content = f.read()
        
        # پشکنین ئەگەر فایلەکە بەتاڵ بوو
        if not cards_content.strip():
            await bot.send_message(chat_id=admin, text="[ERROR] cards.txt is empty!")
            return False

        # ناردنی ناوەرۆکی فایلەکە وەک پەیامی دەق
        await bot.send_message(chat_id=channel, text=cards_content)
        
        await bot.send_message(chat_id=admin, text=f"[SUCCESS] Sent {len(cards_content.splitlines())} cards as text.")
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
        await send_cards_text(bot, CHANNEL_ID, ADMIN_ID)
        await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
