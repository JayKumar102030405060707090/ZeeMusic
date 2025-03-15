import os
from pyrogram import Client, filters
from pyrogram.types import Message

COOKIES_PATH = "cookies/cookies.txt"

def is_cookie_valid():
    return os.path.exists(COOKIES_PATH) and os.path.getsize(COOKIES_PATH) > 0

@Client.on_message(filters.command("checkcookies") & filters.user(7168729089))
async def check_cookies(client: Client, message: Message):
    if is_cookie_valid():
        await message.reply("✅ YouTube cookies are valid and working fine.")
    else:
        await message.reply(
            "⚠️ YT Cookies Expired ❗️\n\n🔄 Change your cookies as soon as possible.\n✅ Must Use Valid Cookies."
        )
