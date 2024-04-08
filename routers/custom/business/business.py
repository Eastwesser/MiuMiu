import datetime
import json
import os
import re
from datetime import datetime, timedelta

from aiogram.enums import ParseMode
from langdetect import detect
import openai
import pytz
import requests
import wikipedia
from aiogram import Bot, F
from aiogram import Router
from aiogram import types, Dispatcher
from aiogram import BaseMiddleware
from aiogram.filters.callback_data import CallbackData
from aiogram.types import TelegramObject
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, CallbackQuery
from currency_converter import CurrencyConverter
from dotenv import load_dotenv
from enum import Enum, auto
from typing import Any, Awaitable, Callable, Dict
from forex_python.converter import CurrencyRates
from aiogram.types import ContentType


from pydantic import BaseModel
from typing import Optional

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
forecast_api = os.getenv('WEATHER_API_TOKEN')
nasa_api = os.getenv('NASA_API_TOKEN')
openai.api_key = os.getenv('OPEN_AI_TOKEN')
deep_ai_key = os.getenv('DEEP_AI_TOKEN')

bot = Bot(token=bot_token)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

currency_converter = CurrencyRates()

data_amount = 0

router = Router(name=__name__)

# WEATHER CONFIG
weather_translations = {
    'Clouds': 'Облачно',
    'Rain': 'Дождь',
    'Snow': 'Снег',
    'Clear': 'Ясно',
    'Haze': 'Туманность',
    'Thunderstorm': 'Гроза',
}

weather_stickers = {
    'Clear': {
        'Утро': 'CAACAgIAAxkBAUDB12XhRMzJqlfh6bg0AU79cYy6Dj_IAALQTAACcSwJSzt9H5-I732HNAQ',
        'День': 'CAACAgIAAxkBAUDBumXhRLi-4D1H43ATD0L1sQ5HhlayAAL-RAAC8fcAAUvf1wyCaqkS_TQE',
        'Вечер': 'CAACAgIAAxkBAUDD2WXhSYxNazCT1hrLpiH3y_GnsLyUAAIYPAACCK4ISzqitpbMjvkxNAQ',
        'Ночь': 'CAACAgIAAxkBAUDB1WXhRMyBxsb7-_XlM4nIuZ4O0qF5AAIxQgACoYgISxirdYdDDa4oNAQ',
    },
    'Rain': 'CAACAgIAAxkBAUDBzmXhRMRBmY92FRMRI9JK_draMYp9AAKUSQACkYcJSw5Yj8ylF0UlNAQ',
    'Snow': 'CAACAgIAAxkBAUDB0GXhRMTa0qg4xyt7pe1vbm09yVgVAAIjSgACXqgAAUt2KFQ_2fGcvDQE',
    'Clouds': 'CAACAgIAAxkBAUDBzGXhRMI9efQqeoUPB0D4uc_7JzeIAAIVPgACECAAAUtq2Fb4XBOYljQE',
    'Haze': 'CAACAgIAAxkBAUQ2vWXu-ZD0GfGckxR7DftiETUJv1QPAALYRQACEhF5SwJG5A-JLtxBNAQ',
    'Thunderstorm': 'CAACAgIAAxkBAUQ3JWXu-33Dzxg33jkftlwk4Ua1g9FrAAKtQQACOb94Sw6ttB1BXQOCNAQ',
}


class WeatherQuery(StatesGroup):
    WaitingForCity = State()


class Questioning(StatesGroup):
    Asking = State()


class ConversionState(StatesGroup):
    AWAITING_AMOUNT = State()
    AWAITING_CURRENCY_PAIR = State()

class CurrencyCallbackFactory(CallbackData, prefix="currency"):
    currency_from: str
    currency_to: str

class CurrencyConversionInput(BaseModel):
    amount: int

class CurrencyPair(BaseModel):
    currency_from: str
    currency_to: str

class ConversionStateData(BaseModel):
    amount: Optional[int] = None
    currency_pair: Optional[CurrencyPair] = None

class ConversionState(BaseModel):
    awaiting_amount: Optional[CurrencyConversionInput] = None
    awaiting_currency_pair: Optional[CurrencyPair] = None
    data: Optional[ConversionStateData] = None

class LanguageState(StatesGroup):
    choose_language = State()
    question = State()

storage = MemoryStorage()

LANGUAGES = ['ru', 'en', 'de', 'es', 'fr', 'hu']

city_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text="/weather Москва")
    ]
])


@router.message(Command("weather_start", prefix="/!%"))
async def weather_start(message: Message, state: FSMContext):
    await message.answer(
        text="Привет! Нажмите кнопку, чтобы выбрать погоду в Москве,\n"
             "либо введите вручную /weather Город,\n"
             "чтобы узнать температуру в другом городе!",
        reply_markup=city_keyboard,
    )
    await state.set_state(WeatherQuery.WaitingForCity)


@router.message(WeatherQuery.WaitingForCity, F.text.in_(city_keyboard))
async def ask_city(message: Message, state: FSMContext):
    await state.update_data(ask_city=message.text.lower())
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите название города:",
        reply_markup=city_keyboard,
    )
    await state.set_state(WeatherQuery.WaitingForCity)


@router.message(Command("weather"))
async def get_weather_command(message: types.Message):
    print("Weather command received!")  # Check if the handler is being triggered
    command_parts = message.text.split(maxsplit=1)
    if len(command_parts) > 1:
        city = command_parts[1]
        print("City:", city)  # Check if the city is extracted correctly
        await get_weather(message, city)
    else:
        await message.reply("Please specify a city after the command.")


async def get_weather(message: types.Message, city: str):
    res = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={forecast_api}&units=metric'
    )
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data['main']['temp']
        pressure_hPa = data['main']['pressure']
        pressure_mmHg = round(pressure_hPa * 0.750062, 2)

        pressure_messages = {
            pressure_mmHg > 755: 'Повышенное',
            730 < pressure_mmHg <= 755: 'Умеренное',
            pressure_mmHg <= 730: 'Пониженное'
        }

        pressure_message = next((msg for condition, msg in pressure_messages.items() if condition),
                                'Данные о давлении недоступны!')

        weather_kind = data['weather'][0]['main']

        # Get the local time and timezone
        timezone_offset = timedelta(seconds=data['timezone'])
        city_timezone = pytz.FixedOffset(int(timezone_offset.total_seconds() / 60))
        local_time = datetime.now(city_timezone)

        if 6 <= local_time.hour < 12:
            current_time_range = 'Утро'
        elif 12 <= local_time.hour < 18:
            current_time_range = 'День'
        elif 18 <= local_time.hour < 24:
            current_time_range = 'Вечер'
        else:
            current_time_range = 'Ночь'

        current_time_str = local_time.strftime('%H:%M')

        if isinstance(weather_stickers[weather_kind], dict):
            sticker_id = weather_stickers[weather_kind].get(current_time_range)
        else:
            sticker_id = weather_stickers[weather_kind]

        if sticker_id:
            await message.answer_sticker(sticker_id)

        # Reply with the weather information
        await message.reply(
            f"Температура сейчас: {temp}°C\n"
            f"{pressure_message} давление: {pressure_mmHg} мм рт ст\n"
            f"Местное время суток: {current_time_range}, {current_time_str}\n"
            f"{weather_translations.get(weather_kind, 'Ясно')}"
        )

    else:
        print(f"Ошибка при запросе: {res.status_code}")
        await message.reply("Такого города нет. Введите существующий город, пожалуйста.")


# NASA - MAGNETIC SOLAR STORMS =========================================================================================
@router.message(Command("magnetic_storm", prefix="!/"))
async def get_magnetic_storm_command(message: types.Message):
    await get_magnetic_storm_data(message)


async def fetch_geomagnetic_storm_data(api_key: str):
    """Fetch geomagnetic storm data from NASA API."""
    url = "https://api.nasa.gov/DONKI/GST"
    params = {'api_key': api_key}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("Error: HTTP status code", response.status_code)
            return None
    except requests.RequestException as e:
        print("Error fetching data:", e)
        return None


async def format_geomagnetic_storm_data(storm_info: list[dict]) -> str:
    """Format geomagnetic storm data for display."""
    formatted_message = "Магнитные бури:\n\n"

    # Sort the storm information based on start time in descending order
    sorted_storms = sorted(storm_info, key=lambda x: x.get('startTime'), reverse=True)

    # Select the most recent storm
    recent_storm = sorted_storms[0] if sorted_storms else None

    if recent_storm:
        gst_id = recent_storm.get('gstID')
        start_time = recent_storm.get('startTime')
        kp_index_data = recent_storm.get('allKpIndex', [{'kpIndex': 'N/A', 'source': 'N/A'}])[0]
        kp_index = kp_index_data.get('kpIndex', 'N/A')
        source = kp_index_data.get('source', 'N/A')
        link = recent_storm.get('link')

        formatted_storm = (
            f"ID бури: {gst_id}\n"
            f"Начало: {start_time}\n"
            f"Kp индекс: {kp_index}\n"
            f"Источник: {source}\n"
            f"Ссылка: {link}\n\n"
        )
        formatted_message += formatted_storm
    else:
        formatted_message += "Нет данных о магнитных бурях в настоящее время."

    return formatted_message


async def send_long_message(message: types.Message, text: str):
    """Send a long message by splitting it into parts."""
    max_length = 4096
    if len(text) <= max_length:
        await message.reply(text)
    else:
        parts = [text[i:i + max_length] for i in range(0, len(text), max_length)]
        for part in parts:
            await message.reply(part)


async def get_magnetic_storm_data(message: types.Message):
    geomagnetic_storm_info = await fetch_geomagnetic_storm_data(nasa_api)
    if geomagnetic_storm_info:
        formatted_storm_message = await format_geomagnetic_storm_data(geomagnetic_storm_info)
        await send_long_message(message, formatted_storm_message)
    else:
        await send_long_message(message, "Нет данных о магнитных бурях в настоящее время.")


# OPEN AI ChatGPT 3.5 (UNCOMMENT IF NEEDED) =============================================================================
# async def ask_chatgpt(question):
#     response = openai.Completion.create(
#         engine="text-davinci-002",  # current version, change if needed
#         prompt=question,
#         max_tokens=1500
#     )
#     return response.choices[0].text.strip()
#
#
# # Modify your existing function to handle asking questions
# @router.message(Command("ask_question", prefix="/!%"))
# async def start_questioning(message: types.Message, state: FSMContext):
#     await state.set_state(Questioning.Asking)
#     await message.answer(
#         "Привет! Задайте ваш вопрос.",
#         reply_markup=types.ReplyKeyboardRemove(),
#     )
#
# @router.message()
# async def answer_question(message: types.Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state == Questioning.Asking:
#         # Get the user's question
#         question = message.text
#         # Call ChatGPT to answer the question
#         response = await ask_chatgpt(question)
#         await message.answer(response)
#         # Finish the conversation
#         await state.clear()

# DeepL AI =============================================================================================================
# logging.basicConfig(level=logging.DEBUG)
#
# async def ask_gpt_deep_ai(question):
#     try:
#         response = requests.post(
#                 "https://api.deepai.org/api/text-generator",
#                 files={'text': question},
#                 headers={'api-key': deep_ai_key}
#             )
#
#
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         response_json = response.json()
#         output = response_json.get("output")
#         if output is None:
#             logging.error("DeepAI API response did not contain 'output' field")
#             return "Sorry, I couldn't generate a response at the moment."
#         return output
#     except requests.exceptions.HTTPError as e:
#         logging.error(f"DeepAI API returned HTTP error: {e.response.status_code}")
#         return "Sorry, an error occurred while processing your request."
#     except Exception as e:
#         logging.exception("An error occurred while calling the DeepAI API")
#         return "Sorry, an error occurred while processing your request."
#
# CURRENCY CONVERTER ===================================================================================================
# Command to start currency conversion
# @router.message(Command("convert"))
# async def start_conversion(message: Message, state: FSMContext):
#     await message.answer("Please enter the amount")
#     await state.set_state(ConversionState.AWAITING_AMOUNT)
#
# # Handler for receiving the amount
# @router.message(state=ConversionState.AWAITING_AMOUNT)
# async def process_amount(message: Message, state: FSMContext):
#     try:
#         amount = float(message.text.strip())
#     except ValueError:
#         await message.answer('Please enter a valid number')
#         return
#
#     if amount <= 0:
#         await message.answer('Please enter a number greater than 0')
#         return
#
#     keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
#         [KeyboardButton(text='USD/EUR'), KeyboardButton(text='EUR/USD')],
#         [KeyboardButton(text='USD/GBP'), KeyboardButton(text='Other')]
#     ])
#
#     await message.answer('Please select the currency pair', reply_markup=keyboard_markup)
#     await state.update_data(amount=amount)
#     await state.set_state(ConversionState.AWAITING_CURRENCY_PAIR)
#
# # Handler for processing currency pair selection
# @router.message(state=ConversionState.AWAITING_CURRENCY_PAIR)
# async def process_currency_pair(message: Message, state: FSMContext):
#     currency_pairs = {
#         'USD/EUR': ('USD', 'EUR'),
#         'EUR/USD': ('EUR', 'USD'),
#         'USD/GBP': ('USD', 'GBP')
#     }
#
#     selected_currency_pair = message.text.upper()
#
#     if selected_currency_pair in currency_pairs:
#         amount_data = await state.get_data()
#         amount = amount_data.get('amount')
#         currency_from, currency_to = currency_pairs[selected_currency_pair]
#         result = currency_converter.convert(currency_from, currency_to, amount)
#         await message.answer(f'Result: {round(result, 2)}. You can enter the amount again!')
#         await state.clear()
#     else:
#         await message.answer('Invalid currency pair. Please select from the options provided.')
#
# # Run the bot
#         await state.set_state(ConversionState.AWAITING_AMOUNT)

# ======================================================================================================================
# Initialize Wikipedia API
class LanguageState(StatesGroup):
    choose_language = State()  # State for choosing language
    english = State()  # State for English language
    russian = State()  # State for Russian language
    stop_wiki = State()  # State for stopping Wikipedia

# Define a new callback data factory for the "clear_wiki_state" button
class ClearWikiCallbackFactory(CallbackData, prefix="clear_wiki"):
    pass

class BackCallbackFactory(CallbackData, prefix="back"):
    pass

# Keyboard for language selection
language_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="English"),
            KeyboardButton(text="Russian"),
        ],
])

clear_state_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Stop asking Wiki"),
        ],
    ],
)

# Command handler for /wiki command
@router.message(Command("wiki", prefix="/!%"))
async def welcome_wiki(message: types.Message, state: FSMContext):
    await state.set_state(LanguageState.choose_language)
    await message.answer(
        "Now we can use Wikipedia to parse simple info.\n"
        "Please select your language. ^w^",
        reply_markup=language_keyboard
    )

@router.message(LanguageState.choose_language, F.text.in_(["English", "Russian"]))
async def select_language(message: types.Message, state: FSMContext):
    language = message.text.lower()
    await state.update_data(language=language)
    if language == "english":
        await state.set_state(LanguageState.english)
        await message.answer("You selected English language.\n"
                             "Ask 1-2 words or press 'Back' to clear the state:",
                             reply_markup=clear_state_keyboard)
    elif language == "russian":
        await state.set_state(LanguageState.russian)
        await message.answer("Вы выбрали русский язык.\n"
                             "Введите запрос в 1-2 слова или нажмите на кнопку, чтобы очистить состояние:",
                             reply_markup=clear_state_keyboard)

# Message handler for English language
@router.message(LanguageState.english)
async def handle_english(message: types.Message, state: FSMContext):
    wikipedia.set_lang("en")
    query = message.text
    try:
        search_results = wikipedia.search(query)
        if search_results:
            page = wikipedia.page(search_results[0])
            await message.answer(page.summary)
#            await state.clear()
        else:
            await message.answer('No information found for this query!\n'
                                 'Ask 1-2 words!')
    except Exception as e:
        await message.answer('No information found for this query!\n'
                             'Ask 1-2 words!')

# Message handler for Russian language
@router.message(LanguageState.russian)
async def handle_russian(message: types.Message, state: FSMContext):
    wikipedia.set_lang("ru")
    query = message.text
    try:
        search_results = wikipedia.search(query)
        if search_results:
            page = wikipedia.page(search_results[0])
            await message.answer(page.summary)
#            await state.clear()
        else:
            await message.answer('Нет информации по вашему запросу!\n'
                                 'Введите запрос в 1-2 слова!')
    except Exception as e:
        await message.answer('Нет информации по вашему запросу!\n'
                             'Введите запрос в 1-2 слова!')

@router.message(LanguageState.choose_language, F.text == "Stop asking Wiki")
async def stop_wiki(message: types.Message, state: FSMContext):
    await state.set_state(LanguageState.stop_wiki)  # Set the new state
    await message.answer("Are you sure you want to stop using Wikipedia?\n"
                         "Type /stop_wiki_confirm to confirm or /start to return to the main menu.")

@router.message(LanguageState.stop_wiki, F.text == "/stop_wiki_confirm")
async def confirm_stop_wiki(message: types.Message, state: FSMContext):
    await state.clear()  # Clear all states
    await message.answer("You won't receive Wikipedia updates anymore.\n"
                         "Returning to the main menu.")
    await welcome_wiki(message, state)  # Call the function to return to the main menu

@router.message(LanguageState.choose_language, ~F.text.in_(["English", "Russian", "Stop asking Wiki"]))
async def invalid_language(message: types.Message, state: FSMContext):
    await message.answer("Please select a language using the provided keyboard or exit the wiki state.")

@router.message(LanguageState.stop_wiki, ~F.text == "/stop_wiki_confirm")
async def invalid_stop_wiki(message: types.Message, state: FSMContext):
    await message.answer("Action canceled.")
    await welcome_wiki(message, state)
