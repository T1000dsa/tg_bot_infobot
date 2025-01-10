from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from lexicon_data.lexicon import LEXICON
from services_data.weather_report import Weather, format_date
from datetime import datetime as dt
from keyboards_data.keyboards_reply import keyboard_reply
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.filters import Command, CommandStart, StateFilter
import logging
from services_data import currency, currency_crypto, bonds, eco_stat
from database_data.database import do_save, check, show_it
from config_data.config import Config, load_config

class FSMFillWeather(StatesGroup):
    weather = State()

class FSMFillQuotes(StatesGroup):
    quotes = State()

router = Router()
logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.DEBUG,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

config:Config = load_config()

@router.message(F.text == '/start', StateFilter(default_state))
async def start_bot_processing(message:Message):
    some_dict = {}
    users_db = show_it()
    await message.answer(text=LEXICON['start'])

    if message.from_user.id not in users_db:
        some_dict['user_id'],some_dict['user_name'], \
        some_dict['is_bot'], some_dict['status'], \
        some_dict['language'] = message.from_user.id, message.from_user.first_name, \
        message.from_user.is_bot, None, \
        message.from_user.language_code
        if check(f'SELECT COUNT(*) FROM {config.db.database_table} WHERE user_id = {message.from_user.id};') == False:
            do_save(some_dict)
        else:
            print(LEXICON['In_database'])

@router.message(F.text == '/help', StateFilter(default_state))
async def help_bot_processing(message:Message):
    await message.answer(text=LEXICON['help'])

@router.message(F.text == '/weather', StateFilter(default_state))
async def weather_bot_processing(message:Message, state: FSMContext):
    await message.answer(text=LEXICON['entry'], reply_markup=keyboard_reply)
    await state.set_state(FSMFillWeather.weather)


@router.message(~StateFilter(default_state), StateFilter(FSMFillWeather))
async def weather_state_bot_processing(message:Message, state: FSMContext):
    try:
        if message.text == LEXICON['button_1']:
            await state.clear()
            await message.answer(text=LEXICON['enough'],reply_markup=ReplyKeyboardRemove())
        else:
            examp = Weather(message.text)
            result = examp.giveforecast()
            city, country, temp, description, date = result[0], result[1], result[2], result[3], dt.strftime(result[4], format_date)
            await message.answer(text=f"{LEXICON['city']}: {city}\n"
                                f"{LEXICON['country']}: {country}\n"
                                f"{LEXICON['temp']}: {temp}C°\n"
                                f"{LEXICON['weath']}: {description}\n"
                                f"{LEXICON['time_res']}: {date}\n",
                                reply_markup=keyboard_reply)
    except(KeyError) as err:
        print(err)
        await message.answer(text=LEXICON['wrong_city'],
                             reply_markup=keyboard_reply)


@router.message(F.text == '/weather_main', StateFilter(default_state))
async def weather_main_bot_processing(message:Message):
    examp = Weather()
    result = examp.main_cities()
    txt = '\n\n'.join([f'{i[0]} - {LEXICON["temp"]}: {i[2]}C°\n'
                       f'{LEXICON["country"]}: {i[1]}\n'
                       f'{LEXICON["weath"]}: {i[3]}\n'
                       f'{LEXICON["time_res"]}: {dt.strftime(i[4], format_date)}' for i in result])
    await message.answer(text=txt)

@router.message(F.text == '/current', StateFilter(default_state))
async def current_bot_processing(message:Message):
    result = currency.do_request()
    time, target, quotes = result['timestamp'], \
    result['source'], \
    '\n'.join([f'{i}: {k}' for i, k in result['quotes'].items()])
    await message.answer(text=f'{dt.fromtimestamp(time)}\n'
                         f'{LEXICON["target"]}: {target}\n'
                         f'{quotes}')


@router.message(F.text == '/crypto', StateFilter(default_state))
async def quotes_bot_processing(message:Message):
    result = currency_crypto.do_request_cry()
    time, target,  quotes = result['timestamp'], \
    result['target'], \
    '\n'.join([f'{i}: {k}' for i, k in result['rates'].items()])
    await message.answer(text=f'{dt.fromtimestamp(time)}\n'
                         f'{LEXICON["target"]}: {target}\n'
                         f'{quotes}')



@router.message(F.text == '/quotes', StateFilter(default_state))
async def quotes_bot_processing(message:Message, state:FSMContext):
    await state.set_state(FSMFillQuotes.quotes)
    await message.answer(text=LEXICON['quot_wait'], reply_markup=keyboard_reply)


@router.message(~StateFilter(default_state), StateFilter(FSMFillQuotes))
async def quotes_state_bot_processing(message:Message, state: FSMContext):
    try:
        if message.text == LEXICON['button_1']:
            await state.clear()
            await message.answer(text=LEXICON['enough'],reply_markup=ReplyKeyboardRemove())
        else:
            exemplar = bonds.Quotes()
            result = exemplar.show_it(message.text.upper())
            company = result[0]
            last = [(i, k) for i, k in result[1].items() if i == max(result[1])][0]
            date_ = last[0]
            data_0_ = last[1]['1. open']
            data_1_ = last[1]['4. close']
            await message.answer(text=f'{LEXICON["comp_tk"]}: {company}\n'
                                 f'Дата: {date_}\n'
                                 f'Старт: {data_0_}\n'
                                 f'Закрытие: {data_1_}',
                                reply_markup=keyboard_reply)
    except(KeyError) as err:
        print(err)
        logger.warning('Выходим из %s', __name__)
        await message.answer(text=LEXICON['wrong_ticket'],
                             reply_markup=keyboard_reply)
        

@router.message(F.text == '/eco_stat', StateFilter(default_state))
async def eco_stat_processing(message:Message):
    some_data_ = eco_stat.Eco_data()
    result_ = some_data_.give_data()
    await message.answer(text=result_)