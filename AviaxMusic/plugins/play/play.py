import random
import string

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message
from pytgcalls.exceptions import NoActiveGroupCall

import config
from AviaxMusic import Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app
from AviaxMusic.core.call import Aviax
from AviaxMusic.utils import seconds_to_min, time_to_seconds
from AviaxMusic.utils.channelplay import get_channeplayCB
from AviaxMusic.utils.decorators.language import languageCB
from AviaxMusic.utils.decorators.play import PlayWrapper
from AviaxMusic.utils.inline import playlist_markup
from AviaxMusic.utils.logger import play_logs
from AviaxMusic.utils.stream.stream import stream
from config import BANNED_USERS, DURATION_LIMIT, DURATION_LIMIT_MIN, lyrical


@app.on_message(filters.command(["play"]) & filters.group & ~BANNED_USERS)
@PlayWrapper
async def play_command(client, message: Message, _, chat_id, video, channel, playmode, url, fplay):
    mystic = await message.reply_text(_["play_2"].format(channel) if channel else _["play_1"])

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    details = None
    source = None

    query = " ".join(message.command[1:]) if not url else url
    if not query:
        return await mystic.edit_text("कृपया एक गाने का नाम दें।")

    # 1️⃣ Spotify
    try:
        details = await Spotify.track(query)
        source = "Spotify"
    except:
        pass

    # 2️⃣ Apple Music
    if not details:
        try:
            details = await Apple.track(query)
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

    # 5️⃣ YouTube (Last Fallback)
    if not details:
        try:
            details, _ = await YouTube.track(query)
            source = "YouTube"
        except:
            return await mystic.edit_text("कोई भी गाना नहीं मिला।")

    # ✅ Duration Check
    if details.get("duration_min"):
        duration_sec = time_to_seconds(details["duration_min"])
        if duration_sec > DURATION_LIMIT:
            return await mystic.edit_text(
                f"⚠️ गाने की अवधि {DURATION_LIMIT_MIN} मिनट से अधिक है।"
            )

    # ✅ Stream the Song
    try:
        await stream(
            _=None,
            message=mystic,
            user_id=user_id,
            details=details,
            chat_id=chat_id,
            user_name=user_name,
            original_chat_id=message.chat.id,
            streamtype=source.lower(),
            forceplay=fplay,
        )
        await mystic.edit_text(f"✅ {source} से गाना प्ले हो रहा है: {details['title']}")
    except Exception as e:
        print(f"Error: {e}")
        await mystic.edit_text(f"🚫 गाना प्ले करने में असफल। Error: {e}")

    return await play_logs(message, streamtype=source.lower())
