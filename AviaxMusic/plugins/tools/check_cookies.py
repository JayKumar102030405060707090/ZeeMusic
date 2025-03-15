from pyrogram import Client, filters
from pyrogram.types import Message

from AviaxMusic import app
from config import BANNED_USERS

@app.on_message(filters.command("checkcookies") & ~BANNED_USERS)
async def check_cookies(client: Client, message: Message):
    try:
        with open("cookies/cookies.txt", "r") as file:
            cookies = file.read()

        if cookies:
            await message.reply("✅ Cookies are present and loaded successfully.")
        else:
            await message.reply("⚠️ Cookies file is empty.")
    except FileNotFoundError:
        await message.reply("❌ Cookies file not found!")
