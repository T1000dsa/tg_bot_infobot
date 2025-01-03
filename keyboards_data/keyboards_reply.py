from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from lexicon_data.lexicon import LEXICON

button_1 = KeyboardButton(
    text=LEXICON['button_1']
)

keyboard_reply = ReplyKeyboardMarkup(
    keyboard=[[button_1]],
    resize_keyboard=True
)
