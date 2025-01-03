from aiogram import F, Router, types
from aiogram.types import CallbackQuery, Message
from lexicon_data.lexicon import LEXICON
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter
from keyboards_data.keyboard_location import keyboard_loc
import logging
from filters_data.filters import IsAdmin
from database_data.database import show_it


router = Router()
logger = logging.getLogger(__name__)

logging.basicConfig(
        level=logging.DEBUG,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

@router.message(F.text=='/location')
async def admin_list_processing(message:Message):
    await message.answer('Отправить данные о геолокации?', reply_markup=keyboard_loc)

@router.message(StateFilter(default_state), F.content_type == 'Location')
async def admin_list_processing(message:Message):
    lat = message.location.latitude
    lon = message.location.longitude
    reply = "latitude:  {}\nlongitude: {}".format(lat, lon)
    await message.answer(reply, reply_markup=types.ReplyKeyboardRemove())


@router.message(F.text == '/show', StateFilter(default_state), IsAdmin())
async def admin_list_processing(message:Message):
    await message.answer(text=str(show_it()))
    

@router.message(StateFilter(default_state))
async def any_else_messages(message:Message):
    await message.answer(text=LEXICON['any_else'])