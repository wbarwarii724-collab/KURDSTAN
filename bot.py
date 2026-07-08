from telethon import TelegramClient, events
import asyncio
from telethon.sessions import StringSession

# ========== ڕێکخستنەکان ==========
api_id = 33790522
api_hash = "00e4131295f55452e143c06099c1ddae"
phone = "+96407504399022"  # ئەمە بگۆڕە بۆ ژمارەی مۆبایلی ڕاست
# ===================================

SOURCE_CHANNEL = "@WarnisxCcScrap"
TARGET_CHANNEL = "@Cc428Kurd"

client = TelegramClient(StringSession(), api_id, api_hash)

async def main():
    await client.start(phone)
    print("✅ سەرکەوتووانە چووە ناوەوە!")

    async for message in client.iter_messages(SOURCE_CHANNEL, limit=1):
        if message.text:
            await client.send_message(TARGET_CHANNEL, message.text)
            print(f"✅ پەیام کۆپی کرا بۆ {TARGET_CHANNEL}!")
        elif message.photo:
            await client.send_file(TARGET_CHANNEL, message.photo, caption=message.caption)
            print(f"✅ وێنە کۆپی کرا بۆ {TARGET_CHANNEL}!")

asyncio.run(main())
