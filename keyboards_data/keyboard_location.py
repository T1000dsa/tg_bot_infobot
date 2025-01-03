from aiogram import Bot, Dispatcher, types, utils


button = types.KeyboardButton(
    text="Share Position", 
    request_location=True
    )

keyboard_loc = types.ReplyKeyboardMarkup(
    keyboard=[[button]],
    resize_keyboard=True
    )
