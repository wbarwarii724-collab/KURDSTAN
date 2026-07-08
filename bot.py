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
    "414582": {"bank": "ICICI Bank", "country": "India 🇮🇳"},
    "401717": {"bank": "HDFC Bank", "country": "India 🇮🇳"},
    "519522": {"bank": "Axis Bank", "country": "India 🇮🇳"},
    "417431": {"bank": "State Bank of India", "country": "India 🇮🇳"},
    "453253": {"bank": "Kotak Mahindra", "country": "India 🇮🇳"},
    "454784": {"bank": "Yes Bank", "country": "India 🇮🇳"},
    "484578": {"bank": "IndusInd Bank", "country": "India 🇮🇳"},
    "512252": {"bank": "Emirates NBD", "country": "UAE 🇦🇪"},
    "518414": {"bank": "Abu Dhabi Commercial Bank", "country": "UAE 🇦🇪"},
    "554809": {"bank": "Dubai Islamic Bank", "country": "UAE 🇦🇪"},
    "542252": {"bank": "Abu Dhabi Islamic Bank", "country": "UAE 🇦🇪"},
    "539811": {"bank": "Barclays Bank", "country": "United Kingdom 🇬🇧"},
    "513143": {"bank": "Lloyds Bank", "country": "United Kingdom 🇬🇧"},
    "549041": {"bank": "HSBC UK", "country": "United Kingdom 🇬🇧"},
    "554702": {"bank": "NatWest", "country": "United Kingdom 🇬🇧"},
    "555384": {"bank": "Santander UK", "country": "United Kingdom 🇬🇧"},
    "481446": {"bank": "Nationwide", "country": "United Kingdom 🇬🇧"},
    "418251": {"bank": "Royal Bank of Canada", "country": "Canada 🇨🇦"},
    "406933": {"bank": "TD Bank", "country": "Canada 🇨🇦"},
    "451083": {"bank": "Scotiabank", "country": "Canada 🇨🇦"},
    "486559": {"bank": "Bank of Montreal", "country": "Canada 🇨🇦"},
    "486109": {"bank": "CIBC", "country": "Canada 🇨🇦"},
    "504435": {"bank": "Deutsche Bank", "country": "Germany 🇩🇪"},
    "514339": {"bank": "Commerzbank", "country": "Germany 🇩🇪"},
    "509431": {"bank": "BNP Paribas", "country": "France 🇫🇷"},
    "402891": {"bank": "Société Générale", "country": "France 🇫🇷"},
    "406976": {"bank": "Crédit Agricole", "country": "France 🇫🇷"},
    "541722": {"bank": "Commonwealth Bank", "country": "Australia 🇦🇺"},
    "482878": {"bank": "Westpac", "country": "Australia 🇦🇺"},
    "483396": {"bank": "ANZ", "country": "Australia 🇦🇺"},
    "493423": {"bank": "NAB", "country": "Australia 🇦🇺"},
    "402397": {"bank": "Intesa Sanpaolo", "country": "Italy 🇮🇹"},
    "514454": {"bank": "UniCredit", "country": "Italy 🇮🇹"},
    "453518": {"bank": "Santander", "country": "Spain 🇪🇸"},
    "455615": {"bank": "BBVA", "country": "Spain 🇪🇸"},
    "478753": {"bank": "CaixaBank", "country": "Spain 🇪🇸"},
    "512343": {"bank": "Garanti BBVA", "country": "Turkey 🇹🇷"},
    "518837": {"bank": "Türkiye İş Bankası", "country": "Turkey 🇹🇷"},
    "426694": {"bank": "Akbank", "country": "Turkey 🇹🇷"},
    "502369": {"bank": "Al Rajhi Bank", "country": "Saudi Arabia 🇸🇦"},
    "480178": {"bank": "Bank AlJazira", "country": "Saudi Arabia 🇸🇦"},
    "531066": {"bank": "Riyad Bank", "country": "Saudi Arabia 🇸🇦"},
    "415988": {"bank": "Banamex", "country": "Mexico 🇲🇽"},
    "476600": {"bank": "Banorte", "country": "Mexico 🇲🇽"},
    "454784": {"bank": "MUFG Bank", "country": "Japan 🇯🇵"},
    "554285": {"bank": "Sumitomo Mitsui", "country": "Japan 🇯🇵"},
    "528901": {"bank": "Mizuho Bank", "country": "Japan 🇯🇵"},
    "460210": {"bank": "Standard Bank", "country": "South Africa 🇿🇦"},
    "505323": {"bank": "Nedbank", "country": "South Africa 🇿🇦"},
    "467524": {"bank": "KB Kookmin Bank", "country": "South Korea 🇰🇷"},
    "469214": {"bank": "Shinhan Bank", "country": "South Korea 🇰🇷"},
    "514329": {"bank": "Banco do Brasil", "country": "Brazil 🇧🇷"},
    "493060": {"bank": "Itaú Unibanco", "country": "Brazil 🇧🇷"},
    "505759": {"bank": "SEB", "country": "Sweden 🇸🇪"},
    "504965": {"bank": "Swedbank", "country": "Sweden 🇸🇪"},
    "514771": {"bank": "DNB", "country": "Norway 🇳🇴"},
    "514974": {"bank": "Danske Bank", "country": "Denmark 🇩🇰"},
    "416687": {"bank": "UBS", "country": "Switzerland 🇨🇭"},
    "417547": {"bank": "Credit Suisse", "country": "Switzerland 🇨🇭"},
    "406681": {"bank": "ING Netherlands", "country": "Netherlands 🇳🇱"},
    "512500": {"bank": "ABN AMRO", "country": "Netherlands 🇳🇱"},
    "540534": {"bank": "Bangkok Bank", "country": "Thailand 🇹🇭"},
    "516543": {"bank": "Kasikorn Bank", "country": "Thailand 🇹🇭"},
    "477320": {"bank": "Bank Mandiri", "country": "Indonesia 🇮🇩"},
    "510713": {"bank": "BCA", "country": "Indonesia 🇮🇩"},
    "502155": {"bank": "Maybank", "country": "Malaysia 🇲🇾"},
    "504498": {"bank": "CIMB Bank", "country": "Malaysia 🇲🇾"},
    "547556": {"bank": "Bank of China", "country": "China 🇨🇳"},
    "403052": {"bank": "ICBC", "country": "China 🇨🇳"},
}

def get_card_details(card_number):
    bin_num = card_number[:6]
    if bin_num in BIN_DATABASE:
        return BIN_DATABASE[bin_num]
    if card_number.startswith('4'):
        return {"bank": "Visa International", "country": "Global 🌍"}
    elif card_number.startswith('5'):
        return {"bank": "Mastercard International", "country": "Global 🌍"}
    elif card_number.startswith('3'):
        return {"bank": "Amex International", "country": "Global 🌍"}
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
    
    # تەنها دەق، وێنە لابراوە
    text = (
        f"KURD SCRAPPER\n"
        f"------------------------\n"
        f"Card : {card_number} | {month}/{year} | {cvv}\n"
        f"________________________\n"
        f"Info : MASTERCARD - CREDIT - STANDARD\n"
        f"Bank : {bank}\n"
        f"Country : {country}\n"
        f"------------------------\n"
        f"▷ Developed by: @warven_24 & rojAmedi2"
    )

    try:
        # تەنها send_message بەکاردەهێنین (وێنە نانێرێت)
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
