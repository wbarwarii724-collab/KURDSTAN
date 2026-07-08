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

# ناوی بانک و وڵاتی دڵخوازی خۆت (بگۆڕە بۆ هەر شتێک کە دەتەوێت)
MY_BANK = "ICICI BANK LTD"
MY_COUNTRY = "INDIA 🇮🇳"
# ==============================================

# خوێندنەوەی کارتەکان لە فایلەکەوە
try:
    if os.path.exists('cards.txt'):
        with open('cards.txt', 'r', encoding='utf-8') as f:
            RAW_CARDS = [line.strip() for line in f if line.strip()]
        print(f"✅ Loaded {len(RAW_CARDS)} cards from cards.txt")
    else:
        RAW_CARDS = []
        print("⚠️ Error: cards.txt not found!")
except Exception as e:
    RAW_CARDS = []
    print(f"❌ Error: {e}")

# هەڵبژاردنی کارتێک بە ڕیز (نەک بە ڕێکەوت)
current_index = 0

async def send_card_message(bot, channel, admin):
    global current_index
    
    if not RAW_CARDS:
        await bot.send_message(chat_id=admin, text="[ERROR] No cards found in cards.txt!")
        return False

    # وەرگرتنی کارتی ئێستا
    card_line = RAW_CARDS[current_index]
    parts = card_line.split('|')
    
    if len(parts) >= 4:
        card_number = parts[0].strip()
        month = parts[1].strip()
        year = parts[2].strip()
        cvv = parts[3].strip()
    else:
        await bot.send_message(chat_id=admin, text=f"[ERROR] Invalid format: {card_line}")
        return False

    bin_number = card_number[:6]
    
    # فۆرماتی کارتەکە (تەنها بانک و وڵاتی خۆت)
    text = (
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"● Warnisx Scrapper by @About_Warnisx\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"● CC: {card_number} | {month}/{year} | {cvv}\n"
        f"● BIN: {bin_number}\n"
        f"● Bank: {MY_BANK}\n"
        f"● Country: {MY_COUNTRY}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Developed By @Warnisx"
    )

    try:
        await bot.send_message(chat_id=channel, text=text)
        await bot.send_message(chat_id=admin, text=f"[SUCCESS] Sent card {current_index+1}/{len(RAW_CARDS)}\nBIN: {bin_number}")
        print(f"✅ Sent card {current_index+1}/{len(RAW_CARDS)}: {card_number}")
        
        # بڕۆ بۆ کارتی دواتر
        current_index += 1
        if current_index >= len(RAW_CARDS):
            current_index = 0  # دووبارە لە سەرەتاوە دەست پێبکاتەوە
        
        return True
    except TelegramError as e:
        await bot.send_message(chat_id=admin, text=f"[ERROR] {str(e)}")
        print(f"❌ Error: {e}")
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
        await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
