import json
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio

from AviaxMusic import app
from config import BANNED_USERS

COOKIES_FILE = "cookies/cookies.txt"
WARNING_CHAT_ID = -1002697050263  # Updated chat ID for cookie expiry warning

# ✅ Function to check if cookies are expired
def is_cookie_expired(cookie_file):
    try:
        with open(cookie_file, "r") as file:
            cookies = json.load(file)

        for cookie in cookies:
            if "expiry" in cookie:
                expiry = datetime.fromtimestamp(cookie["expiry"])
                if expiry < datetime.now():
                    return True  # Cookies expired
        return False  # Cookies valid
    except Exception as e:
        print(f"Error checking cookies: {e}")
        return True  # Error means assume cookies expired

# ✅ Manual /checkcookies command
@app.on_message(filters.command("checkcookies") & ~BANNED_USERS)
async def check_cookies(client: Client, message: Message):
    try:
        with open(COOKIES_FILE, "r") as file:
            cookies = file.read()

        if not cookies.strip():
            await message.reply("⚠️ Cookies file is empty.")
        elif is_cookie_expired(COOKIES_FILE):
            await message.reply("❌ Cookies have expired. Please update them!")
        else:
            await message.reply("✅ Cookies are present and valid.")
    except FileNotFoundError:
        await message.reply("❌ Cookies file not found!")

# ✅ Auto check cookies on bot startup
async def auto_check_cookies():
    await asyncio.sleep(5)  # Wait for the bot to fully initialize
    if is_cookie_expired(COOKIES_FILE):
        try:
            await app.send_message(
                chat_id=WARNING_CHAT_ID,
                text="⚠️ **Warning:** Your YouTube cookies have expired! Please update them to avoid downtime."
            )
        except Exception as e:
            print(f"Failed to send warning message: {e}")

# ✅ Run the auto check after bot starts
app.add_handler(filters=None, callback=auto_check_cookies)
