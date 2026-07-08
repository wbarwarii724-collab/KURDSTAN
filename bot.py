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

# فانکشنێک بۆ دروستکردنی ژمارەی کارتی LUHN-ڕاست
def generate_luhn_card(prefix):
    # دروستکردنی ١٥ ژمارەی کۆتایی بە شێوەی هەڕەمەکی
    card_number = [int(x) for x in str(prefix)] + [random.randint(0, 9) for _ in range(15 - len(str(prefix)))]
    
    # ڕێسای Luhn بۆ هەژماردنی ژمارەی کۆتایی (Check Digit)
    for i in range(len(card_number) - 1, -1, -1):
        if i % 2 == 0:
            card_number[i] *= 2
            if card_number[i] > 9:
                card_number[i] -= 9
    
    check_digit = (10 - (sum(card_number) % 10)) % 10
    
    # گەڕاندنەوەی ژمارە تەواوەکە
    full_card = str(prefix) + ''.join([str(random.randint(0, 9)) for _ in range(14 - len(str(prefix)))]) + str(check_digit)
    return full_card

BANKS = [
    "JPMorgan Chase", "Bank of America", "Wells Fargo", "Citibank", "HSBC",
    "Barclays", "Lloyds Bank", "Deutsche Bank", "BNP Paribas", "ING Bank",
    "ICICI Bank", "HDFC Bank", "State Bank of India", "Standard Chartered",
    "MUFG Bank", "Mizuho Bank", "Royal Bank of Canada", "Commonwealth Bank",
    "DBS Bank", "Toronto-Dominion Bank", "United Overseas Bank",
    "AEON THANA SINSAP (THAILAND) PUBLIC COMPANY LIMITED"
]

COUNTRIES = [
    "USA 🇺🇸", "United Kingdom 🇬🇧", "Canada 🇨🇦", "Australia 🇦🇺",
    "Germany 🇩🇪", "France 🇫🇷", "Italy 🇮🇹", "Spain 🇪🇸",
    "Netherlands 🇳🇱", "Sweden 🇸🇪", "Norway 🇳🇴", "Denmark 🇩🇰",
    "Switzerland 🇨🇭", "Austria 🇦🇹", "Portugal 🇵🇹", "Greece 🇬🇷",
    "Turkey 🇹🇷", "UAE 🇦🇪", "Saudi Arabia 🇸🇦", "Qatar 🇶🇦",
    "India 🇮🇳", "China 🇨🇳", "Japan 🇯🇵", "Singapore 🇸🇬",
    "South Africa 🇿🇦", "Brazil 🇧🇷", "Mexico 🇲🇽", "Colombia 🇨🇴",
    "THAILAND [TH] 🇹🇭"
]

CARD_TYPES = [
    "CREDIT | MASTERCARD | STANDARD", 
    "CREDIT | VISA | CLASSIC", 
    "DEBIT | MASTERCARD | GOLD", 
    "DEBIT | VISA | PLATINUM",
    "CREDIT | AMEX | BUSINESS"
]

async def send_card_message(bot, channel, admin):
    card_type = random.choice(CARD_TYPES)
    
    # دروستکردنی ژمارەی کارت بە LUHN و پێشگر (Prefix)
    if "VISA" in card_type:
        card_number = generate_luhn_card(4) # Visa دەست پێدەکات بە 4
    elif "MASTERCARD" in card_type:
        card_number = generate_luhn_card(5) # Mastercard دەست پێدەکات بە 5
    else: 
        card_number = generate_luhn_card(3) # Amex دەست پێدەکات بە 3

    month = str(random.randint(1, 12)).zfill(2)
    year = str(random.randint(2026, 2036))
    cvv = str(random.randint(100, 999))
    bin_number = card_number[:6] # BIN (6 ژمارەی سەرەتا)
    
    bank = random.choice(BANKS)
    country = random.choice(COUNTRIES)
    
    text = (
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"● Warnisx Scrapper by @About_Warnisx\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"● CC: {card_number} | {month}/{year} | {cvv}\n"
        f"● BIN: {bin_number}\n"
        f"● Bank: {bank}\n"
        f"● Country: {country}\n"
        f"● Type: {card_type}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Developed By @Warnisx"
    )

    try:
        await bot.send_message(chat_id=channel, text=text)
        await bot.send_message(chat_id=admin, text=f"[SUCCESS] Sent\nBIN: {bin_number}")
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
