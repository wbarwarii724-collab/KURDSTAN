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

# وێنەی سەرووی پەیامەکە (دەتوانیت ئەمە بگۆڕیت بۆ هەر وێنەیەک کە دەتەوێت)
IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Cristiano_Ronaldo_2018.jpg/220px-Cristiano_Ronaldo_2018.jpg"
# ==============================================

# لیستی تەواوی بانکە جیهانییەکان
BANKS = [
    "JPMorgan Chase Bank, N.A.", "Bank of America, N.A.", "Wells Fargo Bank, N.A.",
    "Citibank, N.A.", "HSBC Bank plc", "Barclays Bank plc", "Lloyds Bank plc",
    "Deutsche Bank AG", "BNP Paribas", "Société Générale", "ING Bank N.V.",
    "ICICI Bank", "HDFC Bank", "State Bank of India", "Standard Chartered Bank",
    "MUFG Bank, Ltd.", "Mizuho Bank, Ltd.", "Sumitomo Mitsui Banking Corporation",
    "Toronto-Dominion Bank", "Royal Bank of Canada", "Commonwealth Bank of Australia",
    "National Australia Bank", "United Overseas Bank", "DBS Bank Ltd."
]

# لیستی تەواوی وڵاتەکان بە ئاڵاکانیان
COUNTRIES = [
    "USA 🇺🇸", "United Kingdom 🇬🇧", "Canada 🇨🇦", "Australia 🇦🇺",
    "Germany 🇩🇪", "France 🇫🇷", "Italy 🇮🇹", "Spain 🇪🇸",
    "Netherlands 🇳🇱", "Belgium 🇧🇪", "Switzerland 🇨🇭", "Sweden 🇸🇪",
    "Norway 🇳🇴", "Denmark 🇩🇰", "Finland 🇫🇮", "Ireland 🇮🇪",
    "Austria 🇦🇹", "Portugal 🇵🇹", "Greece 🇬🇷", "Poland 🇵🇱",
    "Russia 🇷🇺", "Ukraine 🇺🇦", "Turkey 🇹🇷", "UAE 🇦🇪",
    "Saudi Arabia 🇸🇦", "Qatar 🇶🇦", "Kuwait 🇰🇼", "Bahrain 🇧🇭",
    "India 🇮🇳", "China 🇨🇳", "Japan 🇯🇵", "South Korea 🇰🇷",
    "Singapore 🇸🇬", "Malaysia 🇲🇾", "Indonesia 🇮🇩", "Thailand 🇹🇭",
    "Vietnam 🇻🇳", "South Africa 🇿🇦", "Nigeria 🇳🇬", "Mexico 🇲🇽",
    "Brazil 🇧🇷", "Argentina 🇦🇷", "Chile 🇨🇱", "Colombia 🇨🇴"
]

# لیستی جۆرەکانی کارت
CARD_TYPES = ["VISA CREDIT CLASSIC", "VISA DEBIT PLATINUM", "MASTERCARD GOLD", "MASTERCARD PLATINUM", "AMEX BUSINESS"]

async def send_card_message(bot, channel, admin):
    # دروستکردنی کارتی ڕێکەوت
    card_number = f"4{random.randint(100000000000000, 999999999999999)}"
    month = str(random.randint(1, 12)).zfill(2)
    year = str(random.randint(2026, 2036))
    cvv = str(random.randint(100, 999))
    
    # هەڵبژاردنی ڕێکەوت
    bank = random.choice(BANKS)
    country = random.choice(COUNTRIES)
    card_type = random.choice(CARD_TYPES)
    
    # فۆرماتی تەواو پیشەیی وەکو کەناڵەکە
    text = (f"Scrapper Hamody\n"
            f"----------------------------------\n"
            f"Card : {card_number} | {month}/{year} | {cvv}\n"
            f"__________________________________\n"
            f"Info : {card_type}\n"
            f"Bank : {bank}\n"
            f"Country : {country}\n"
            f"----------------------------------\n"
            f"▷ Developed by: HamoDy")

    try:
        # ناردنی وێنە + دەق بە شێوەیەکی جوان
        await bot.send_photo(chat_id=channel, photo=IMAGE_URL, caption=text, parse_mode='HTML')
        await bot.send_message(chat_id=admin, text=f"[SUCCESS] Sent\nBank: {bank}")
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
