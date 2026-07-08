# -*- coding: utf-8 -*-
import asyncio
import logging
from telegram import Bot
from telegram.error import TelegramError

# ===== CONFIG =====
BOT_TOKEN = "8941847443:AAF78KW48MF93ntjK8ROGanD1TiEzc4O1_Q"
SOURCE_CHANNEL = "@hamody_up4"
TARGET_CHANNEL = "@Cc428Kurd"
INTERVAL_SECONDS = 3
# ==============================================

# چالاککردنی لۆگەکان بۆ دۆزینەوەی هەڵەکان
logging.basicConfig(level=logging.INFO)

async def copy_and_send(bot, source, target):
    try:
        logging.info("Checking for new messages...")
        updates = await bot.get_updates()
        
        if updates and updates[-1].channel_post:
            last_post = updates[-1].channel_post
            logging.info(f"Found a post: {last_post.message_id}")
            
            # ناردنی وێنە ئەگەر هەبێت
            if last_post.photo:
                file_id = last_post.photo[-1].file_id
                caption = last_post.caption or ""
                await bot.send_photo(chat_id=target, photo=file_id, caption=caption)
                logging.info(f"✅ Photo + text sent to {target}!")
            
            # ناردنی دەق ئەگەر وێنە نەبێت
            elif last_post.text:
                await bot.send_message(chat_id=target, text=last_post.text)
                logging.info(f"✅ Text sent to {target}!")
            else:
                logging.warning("⚠️ No photo or text found in the post.")
        else:
            logging.info("📭 No new messages found.")
            
    except TelegramError as e:
        logging.error(f"❌ Telegram Error: {e}")
    except Exception as e:
        logging.error(f"❌ General Error: {e}")

async def main():
    bot = Bot(token=BOT_TOKEN)
    while True:
        await copy_and_send(bot, SOURCE_CHANNEL, TARGET_CHANNEL)
        await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
