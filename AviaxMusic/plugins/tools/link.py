from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import (
    ChatAdminRequired,
    ChatInvalid,
    PeerIdInvalid,
    UserNotParticipant,
    InviteHashInvalid,
)
from AviaxMusic import app
from config import BANNED_USERS

# केवल इस यूजर को अनुमति है
AUTHORIZED_USER = 7168729089

@app.on_message(filters.command("link") & ~BANNED_USERS)
async def get_chat_link(client, message: Message):
    # ✅ 1. यूज़र को वेरीफाई करें
    if message.from_user.id != AUTHORIZED_USER:
        return await message.reply_text("❌ आपको इस कमांड का उपयोग करने की अनुमति नहीं है।")

    # ✅ 2. चैट ID चेक करें
    if len(message.command) != 2:
        return await message.reply_text("❌ सही उपयोग: `/link <chat_id>`", quote=True)

    chat_id = message.command[1]

    # ✅ 3. चैट ID का फॉर्मेट चेक करें
    if not chat_id.startswith("-100"):
        return await message.reply_text("❌ चैट ID का फॉर्मेट गलत है। यह '-100' से शुरू होना चाहिए।", quote=True)

    try:
        # ✅ 4. बोट की जानकारी प्राप्त करें
        bot_info = await app.get_me()

        # ✅ 5. ग्रुप और बोट की सदस्यता चेक करें
        chat = await app.get_chat(chat_id)
        bot_member = await app.get_chat_member(chat_id, bot_info.id)

        # ✅ 6. क्या बोट ग्रुप में है?
        if bot_member.status not in ["administrator", "creator"]:
            return await message.reply_text("❌ मैं उस ग्रुप में एडमिन नहीं हूँ।", quote=True)

        # ✅ 7. क्या बोट के पास इनवाइट लिंक बनाने की परमिशन है?
        if not bot_member.can_invite_users:
            return await message.reply_text("❌ मेरे पास इनवाइट लिंक बनाने की अनुमति नहीं है।", quote=True)

        # ✅ 8. यदि लिंक पहले से मौजूद है तो वही उपयोग करें, अन्यथा नया बनाएं
        invite_link = chat.invite_link
        if not invite_link:
            invite_link = await app.export_chat_invite_link(chat_id)

        await message.reply_text(f"✅ **{chat.title}** का इनवाइट लिंक:\n{invite_link}", quote=True)

    except ChatInvalid:
        await message.reply_text("❌ चैट ID गलत है। कृपया सही ID का उपयोग करें।", quote=True)
    except PeerIdInvalid:
        await message.reply_text("❌ चैट ID का फॉर्मेट गलत है।", quote=True)
    except UserNotParticipant:
        await message.reply_text("❌ मैं उस ग्रुप का सदस्य नहीं हूँ।", quote=True)
    except ChatAdminRequired:
        await message.reply_text("❌ मुझे इनवाइट लिंक प्राप्त करने के लिए एडमिन बनाएं।", quote=True)
    except InviteHashInvalid:
        await message.reply_text("❌ इनवाइट लिंक बनाने में समस्या आई। कृपया पुनः प्रयास करें।", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ एक त्रुटि हुई: `{e}`", quote=True)
