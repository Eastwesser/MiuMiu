import datetime
import json
import os
from datetime import datetime, timedelta

import pytz
import requests
from aiogram import Bot
from aiogram import Router, F
from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

bot_token = os.getenv('BOT_TOKEN')
forecast_api = os.getenv('WEATHER_API_TOKEN')
load_dotenv()

bot = Bot(token=bot_token)
dp = Dispatcher()

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
