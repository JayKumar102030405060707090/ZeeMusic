from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, ChatIdInvalid, PeerIdInvalid, RPCError
from AviaxMusic import app
from config import BANNED_USERS

@app.on_message(filters.command("link") & ~BANNED_USERS)
async def get_invite_link(client, message: Message):
    # सिर्फ स्पेसिफिक यूजर को अनुमति
    if message.from_user.id != 7168729089:
        return await message.reply_text("❌ आपको इस कमांड को चलाने की अनुमति नहीं है।", quote=True)

    # चैट ID चेक करना
    if len(message.command) < 2:
        return await message.reply_text("❌ कृपया चैट ID दें।\nउदाहरण: `/link -1001234567890`", quote=True)

    chat_id_input = message.text.split(None, 1)[1].strip()

    # ID को इंटीजर में बदलने की कोशिश
    try:
        chat_id = int(chat_id_input)
    except ValueError:
        chat_id = chat_id_input  # अगर ID पब्लिक username है

    try:
        # चैट की जानकारी प्राप्त करें
        chat = await app.get_chat(chat_id)
        print(f"[DEBUG] Chat Info: {chat}")

        # बोट का मेंबरशिप स्टेटस चेक करें
        bot_member = await app.get_chat_member(chat.id, "me")
        print(f"[DEBUG] Bot Member Status: {bot_member}")

        # बोट एडमिन है या नहीं?
        if bot_member.status != "administrator":
            return await message.reply_text("❌ मैं उस ग्रुप में एडमिन नहीं हूँ।", quote=True)

        # बोट के पास इनवाइट लिंक की अनुमति है या नहीं?
        if not bot_member.privileges or not bot_member.privileges.can_invite_users:
            return await message.reply_text("❌ मेरे पास 'Invite Users via Link' की अनुमति नहीं है।", quote=True)

        # ग्रुप पब्लिक है या प्राइवेट?
        if chat.username:
            invite_link = f"https://t.me/{chat.username}"
            return await message.reply_text(f"✅ इस पब्लिक ग्रुप का लिंक:\n{invite_link}", quote=True)

        # प्राइवेट ग्रुप का इनवाइट लिंक जनरेट करना
        invite_link = await app.export_chat_invite_link(chat.id)
        print(f"[DEBUG] Generated Invite Link: {invite_link}")

        await message.reply_text(f"✅ इस ग्रुप का इनवाइट लिंक:\n{invite_link}", quote=True)

    except ChatIdInvalid:
        return await message.reply_text("❌ दिया गया चैट ID अमान्य है।", quote=True)

    except PeerIdInvalid:
        return await message.reply_text("❌ यह चैट ID एक्सेस नहीं हो पा रही है।", quote=True)

    except ChatAdminRequired:
        return await message.reply_text("❌ मेरे पास इस ग्रुप का इनवाइट लिंक प्राप्त करने की अनुमति नहीं है।", quote=True)

    except UserNotParticipant:
        return await message.reply_text("❌ मैं उस ग्रुप का सदस्य नहीं हूँ।", quote=True)

    except RPCError as e:
        return await message.reply_text(f"❌ Telegram API Error: {e}", quote=True)

    except Exception as e:
        return await message.reply_text(f"❌ कोई अज्ञात त्रुटि हुई: {e}", quote=True)
