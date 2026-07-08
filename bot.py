# -*- coding: utf-8 -*-
import asyncio
from telegram import Bot

# ===== CONFIG =====
BOT_TOKEN = "8941847443:AAF78KW48MF93ntjK8ROGanD1TiEzc4O1_Q"
SOURCE_CHANNEL = "@hamody_up4"
TARGET_CHANNEL = "@DUHOK_CC"
INTERVAL_SECONDS = 3
# ==============================================

async def copy_and_send(bot, source, target):
    try:
        updates = await bot.get_updates()
        if updates and updates[-1].channel_post:
            last_post = updates[-1].channel_post
            
            # ئەگەر پەیامەکە وێنەی هەیە (send_photo)
            if last_post.photo:
                file_id = last_post.photo[-1].file_id
                caption = last_post.caption or ""
                await bot.send_photo(chat_id=target, photo=file_id, caption=caption)
                print(f"✅ Copied photo + text to {target}!")
            
            # ئەگەر پەیامەکە تەنها دەقە (send_message)
            elif last_post.text:
                await bot.send_message(chat_id=target, text=last_post.text)
                print(f"✅ Copied text to {target}!")
                
    except Exception as e:
        print(f"❌ Error: {e}")

async def main():
    bot = Bot(token=BOT_TOKEN)
    while True:
        await copy_and_send(bot, SOURCE_CHANNEL, TARGET_CHANNEL)
        await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
