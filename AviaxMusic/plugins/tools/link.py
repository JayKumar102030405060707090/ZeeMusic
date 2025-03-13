from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import ChatAdminRequired, ChatInvalid, PeerIdInvalid, UserNotParticipant
from AviaxMusic import app
from AviaxMusic.misc import SUDOERS
from config import BANNED_USERS

# Authorized User ID
AUTHORIZED_USER = 7168729089

@app.on_message(filters.command("link") & ~BANNED_USERS)
async def get_chat_link(client, message: Message):
    # Ensure only the authorized user can use the command
    if message.from_user.id != AUTHORIZED_USER:
        return await message.reply_text("You're not authorized to use this command.")

    # Check if chat ID is provided
    if len(message.command) != 2:
        return await message.reply_text("Usage: `/link <chat_id>`", quote=True)

    chat_id = message.command[1]

    try:
        # Fetch chat information
        chat = await app.get_chat(chat_id)
        member = await app.get_chat_member(chat_id, "me")

        # Check if the bot is an admin
        if not member.status in ("administrator", "creator"):
            return await message.reply_text("I'm not an admin in that group.", quote=True)

        # Check if the bot has the invite link permission
        if not member.can_invite_users:
            return await message.reply_text("I don't have permission to generate invite links.", quote=True)

        # Generate and send the invite link
        if chat.invite_link:
            invite_link = chat.invite_link
        else:
            invite_link = await app.export_chat_invite_link(chat_id)
        
        await message.reply_text(f"Invite Link for {chat.title}: {invite_link}", quote=True)

    except ChatInvalid:
        await message.reply_text("Invalid chat ID. Please check and try again.", quote=True)
    except PeerIdInvalid:
        await message.reply_text("Invalid chat ID format. Please provide a correct one.", quote=True)
    except ChatAdminRequired:
        await message.reply_text("I need to be an admin to fetch the invite link.", quote=True)
    except UserNotParticipant:
        await message.reply_text("I'm not a member of that chat.", quote=True)
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}", quote=True)
