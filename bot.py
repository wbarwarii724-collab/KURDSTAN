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

# فانکشنێکی ڕاست و تەواو بۆ دروستکردنی ژمارەی کارتی LUHN (١٦ ڕقە)
def generate_luhn_card(prefix):
    # دەستپێکی ژمارەکە
    card = [int(x) for x in str(prefix)]
    # زیادکردنی ژمارە هەڕەمەکییەکان تا دەگاتە ١٥ ڕقە (ئەمێکس ١٤)
    length = 16 if prefix != 3 else 15
    while len(card) < length - 1:
        card.append(random.randint(0, 9))
    
    # هەژماردنی Check Digit بەپێی ڕێسای Luhn
    total = 0
    for i in range(len(card) - 1, -1, -1):
        digit = card[i]
        if (len(card) - i) % 2 == 0: # لە ڕاستەوە بۆ چەپ، دووەم ژمارە دوو هێندە دەبێت
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    
    check_digit = (10 - (total % 10)) % 10
    card.append(check_digit)
    
    return ''.join(map(str, card))

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
    
    # دروستکردنی ژمارەی کارت بەپێی جۆرەکە
    if "VISA" in card_type:
        card_number = generate_luhn_card(4)
    elif "MASTERCARD" in card_type:
        card_number = generate_luhn_card(5)
    else:
        card_number = generate_luhn_card(3) # AMEX پێویستی بە ١٥ ڕقەیە

    month = str(random.randint(1, 12)).zfill(2)
    year = str(random.randint(2026, 2036))
    cvv = str(random.randint(100, 999))
    bin_number = card_number[:6]
    
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
