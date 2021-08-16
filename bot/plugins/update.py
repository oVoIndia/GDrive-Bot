from bot import SUPPORT_CHAT_LINK
from pyrogram import Client, filters
from bot.config import Messages as tr
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def map(pos):
    if(pos==1):
        button = [
            [InlineKeyboardButton(text = '-->', callback_data = "update+2")]
        ]
    elif(pos==len(tr.UPDATE_MSG)-1):

        button = [
        [
            InlineKeyboardButton(text = 'Support Chat', url = SUPPORT_CHAT_LINK),
            InlineKeyboardButton(text = 'Feature Request', url = "https://github.com/oVoIndia/GDrive-Bot/issues/new")
            ],
            [InlineKeyboardButton(text = '<--', callback_data = f"update+{pos-1}")]
          
        ]
    else:
        button = [
            [
                InlineKeyboardButton(text = '<--', callback_data = f"update+{pos-1}"),
                InlineKeyboardButton(text = '-->', callback_data = f"update+{pos+1}")
            ],
        ]
    return button

@Client.on_message(filters.private & filters.incoming & filters.command(['update', 'up']), group=2)
def _update(client, message):
    client.send_message(chat_id = message.chat.id,
        text = tr.UPDATE_MSG[1],
        disable_web_page_preview=True,
        reply_markup = InlineKeyboardMarkup(map(1)),
        reply_to_message_id = message.message_id
    )


update_callback_filter = filters.create(lambda _, __, query: query.data.startswith('update+'))

@Client.on_callback_query(update_callback_filter)
def update_answer(c, callback_query):
    chat_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    msg = int(callback_query.data.split('+')[1])
    c.edit_message_text(chat_id = chat_id,    message_id = message_id,
        text = tr.UPDATE_MSG[msg],    reply_markup = InlineKeyboardMarkup(map(msg))
    )
