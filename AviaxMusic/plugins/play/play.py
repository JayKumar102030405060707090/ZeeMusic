from pyrogram import filters
from pyrogram.types import Message
from AviaxMusic import Spotify, Apple, SoundCloud, Resso, YouTube, app
from AviaxMusic.utils.stream.stream import stream
from config import BANNED_USERS, DURATION_LIMIT, DURATION_LIMIT_MIN

@app.on_message(filters.command(["play"]) & filters.group & ~BANNED_USERS)
async def play_command(client, message: Message):
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply_text("कृपया एक गाने का नाम दें।")

    mystic = await message.reply_text("🔍 गाना खोजा जा रहा है...")

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    chat_id = message.chat.id
    details = None
    source = None

    # 1️⃣ Spotify
    try:
        details, _ = await Spotify.track(query)
        source = "Spotify"
    except:
        pass

    # 2️⃣ Apple Music
    if not details:
        try:
            details, _ = await Apple.track(query)
            source = "Apple Music"
        except:
            pass

    # 3️⃣ SoundCloud
    if not details:
        try:
            details, _ = await SoundCloud.download(query)
            source = "SoundCloud"
        except:
            pass

    # 4️⃣ Resso
    if not details:
        try:
            details, _ = await Resso.track(query)
            source = "Resso"
        except:
            pass

    # 5️⃣ YouTube (Only if not found elsewhere)
    if not details:
        try:
            details, _ = await YouTube.track(query)
            source = "YouTube"
        except:
            return await mystic.edit_text("⚠️ कोई भी गाना नहीं मिला।")

    # ✅ Duration Check
    if details.get("duration_min"):
        duration_sec = sum(int(x) * 60 ** i for i, x in enumerate(reversed(details["duration_min"].split(":"))))
        if duration_sec > DURATION_LIMIT:
            return await mystic.edit_text(
                f"⚠️ गाने की अवधि {DURATION_LIMIT_MIN} मिनट से अधिक है।"
            )

    # ✅ Stream the Song
    try:
        await stream(
            user_id=user_id,
            details=details,
            chat_id=chat_id,
            user_name=user_name,
            streamtype=source.lower(),
            forceplay=False,
        )
        await mystic.edit_text(f"✅ {source} से गाना प्ले हो रहा है: {details['title']}")
    except Exception as e:
        print(f"Error: {e}")
        await mystic.edit_text(f"🚫 गाना प्ले करने में असफल। Error: {e}")
