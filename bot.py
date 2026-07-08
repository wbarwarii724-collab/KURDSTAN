# -*- coding: utf-8 -*-
import asyncio
import logging
from telegram import Bot
from telegram.error import TelegramError

# ==================== ڕێکخستنەکان ====================
# تۆکنی بۆتەکەت
BOT_TOKEN = "8941847443:AAF78KW48MF93ntjK8ROGanD1TiEzc4O1_Q"

# کەناڵی سەرچاوە (ئەمە گۆڕدرا بۆ WarnisxCcScrap)
SOURCE_CHANNEL = "@WarnisxCcScrap"

# کەناڵی ئامانج (پەیامەکان دەنێردرێن بۆ ئەم کەناڵە)
TARGET_CHANNEL = "@Cc428Kurd"

# ماوەی چاوەڕوانی لە نێوان هەر پەیامێکدا
INTERVAL_SECONDS = 3
# ======================================================

logging.basicConfig(level=logging.INFO)

async def copy_and_send(bot, source, target):
    try:
        logging.info("⏳ چاوەڕوانی پەیامی نوێ...")
        updates = await bot.get_updates()
        
        if updates and updates[-1].channel_post:
            last_post = updates[-1].channel_post
            logging.info(f"✅ پەیامێک دۆزرایەوە: {last_post.message_id}")
            
            if last_post.photo:
                file_id = last_post.photo[-1].file_id
                caption = last_post.caption or ""
                await bot.send_photo(chat_id=target, photo=file_id, caption=caption)
                logging.info(f"📸 وێنە + دەق نێردرا بۆ {target}!")
            
            elif last_post.text:
                await bot.send_message(chat_id=target, text=last_post.text)
                logging.info(f"📝 دەق نێردرا بۆ {target}!")
            
            else:
                logging.warning("⚠️ پەیامەکە نە وێنەی تێدابوو نە دەق.")
        else:
            logging.info("📭 هیچ پەیامێکی نوێ نەدۆزرایەوە.")
            
    except TelegramError as e:
        logging.error(f"❌ هەڵەی تەلەگرام: {e}")
    except Exception as e:
        logging.error(f"❌ هەڵەی گشتی: {e}")

async def main():
    bot = Bot(token=BOT_TOKEN)
    while True:
        await copy_and_send(bot, SOURCE_CHANNEL, TARGET_CHANNEL)
        await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
