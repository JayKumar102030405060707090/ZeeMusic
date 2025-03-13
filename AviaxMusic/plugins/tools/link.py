from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, ChatIdInvalid, PeerIdInvalid
from AviaxMusic import app
from AviaxMusic.misc import SUDOERS
from config import BANNED_USERS

@app.on_message(filters.command("link") & ~BANNED_USERS)
async def get_invite_link(client, message: Message):
    # सिर्फ स्पेसिफिक यूजर को परमिशन
    if message.from_user.id != 7168729089:
        return await message.reply_text("❌ आपके पास इस कमांड को चलाने की अनुमति नहीं है।", quote=True)

    # चैट आईडी एक्सट्रेक्ट करना
    if len(message.command) < 2:
        return await message.reply_text("❌ कृपया चैट आईडी दें।\nउदाहरण: `/link -1001234567890`", quote=True)

    chat_id = message.text.split(None, 1)[1].strip()

    try:
        # बोट का मेंबरशिप स्टेटस चेक करना
        bot_member = await app.get_chat_member(chat_id, "me")
        
        # अगर बोट एडमिन नहीं है
        if bot_member.status != "administrator":
            return await message.reply_text("❌ मैं उस ग्रुप में एडमिन नहीं हूँ।", quote=True)

        # अगर बोट के पास इनवाइट परमिशन नहीं है
        if not bot_member.privileges or not bot_member.privileges.can_invite_users:
            return await message.reply_text("❌ मेरे पास 'Invite Users via Link' की अनुमति नहीं है।", quote=True)

        # इनवाइट लिंक लेना
        invite_link = await app.export_chat_invite_link(chat_id)
        await message.reply_text(f"✅ इस ग्रुप का इनवाइट लिंक:\n{invite_link}", quote=True)

    except UserNotParticipant:
        await message.reply_text("❌ मैं उस ग्रुप का सदस्य नहीं हूँ।", quote=True)

    except ChatAdminRequired:
        await message.reply_text("❌ मेरे पास इस ग्रुप का इनवाइट लिंक प्राप्त करने की अनुमति नहीं है।", quote=True)

    except ChatIdInvalid:
        await message.reply_text("❌ दिया गया चैट ID अमान्य है। कृपया सही ID डालें।", quote=True)

    except PeerIdInvalid:
        await message.reply_text("❌ दिया गया चैट ID अमान्य है।", quote=True)

    except Exception as e:
        await message.reply_text(f"❌ कोई त्रुटि हुई: `{e}`", quote=True)
