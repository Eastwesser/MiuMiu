import os

from aiogram import Bot
from aiogram import Router
from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

bot_token = os.getenv('BOT_TOKEN')
forecast_api = os.getenv('WEATHER_API_TOKEN')
load_dotenv()

bot = Bot(token=bot_token)
dp = Dispatcher()

router = Router(name=__name__)


# CALCULATOR
@router.message(Command("calculator", prefix="/!%"))
async def send_welcome(message: types.Message):
    await message.reply(
        "Hi!\nI'm a calculator bot. "
        "\nYou can perform calculations by sending me commands like: "
        "\n/add 5 3, "
        "\n/subtract 7 2, "
        "\n/multiply 4 6, "
        "\n/divide 8 2."
        "\nPlease, use only integer numbers!"
    )


def make_row_calculator_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(
        keyboard=[row],
        resize_keyboard=True,
    )


@router.message(Command("calculator", prefix="/!%"))
async def send_welcome(message: types.Message):
    calculator_operations = [
        "/add",
        "/subtract",
        "/multiply",
        "/divide",
    ]
    keyboard = make_row_calculator_keyboard(calculator_operations)
    await message.reply("Choose a calculator operation:", reply_markup=keyboard)

    await message.reply(
        "Hi!\nI'm a calculator bot. "
        "\nYou can perform calculations by sending me commands like: "
        "\n/add 5 3, "
        "\n/subtract 7 2, "
        "\n/multiply 4 6, "
        "\n/divide 8 2."
        "\nPlease, use only integer numbers!",
        reply_markup=keyboard
    )


@router.message(Command("add", prefix="/!%"))
async def add(message: types.Message):
    await process_operation(message, '+')


@router.message(Command("subtract", prefix="/!%"))
async def subtract(message: types.Message):
    await process_operation(message, '-')


@router.message(Command("multiply", prefix="/!%"))
async def multiply(message: types.Message):
    await process_operation(message, '*')


@router.message(Command("divide", prefix="/!%"))
async def divide(message: types.Message):
    await process_operation(message, '/')


async def process_operation(message: types.Message, operator: str):
    try:
        command, num1, num2 = message.text.split()
        num1 = float(num1)
        num2 = float(num2)
    except ValueError:
        await message.reply("Invalid input. Please provide two numbers.")
        return

    result = None
    if operator == '+':
        result = round(num1 + num2)
    elif operator == '-':
        result = round(num1 - num2)
    elif operator == '*':
        result = round(num1 * num2)
    elif operator == '/':
        if num2 != 0:
            result = num1 / num2
        else:
            await message.reply("Division by zero is not allowed.")
            return

    await message.reply(f"Result: {result}")


# CONVERTER ============================================================================================================
conversion_functions = {
    "/inches_to_cm": lambda x: x * 2.54,
    "/cm_to_inches": lambda x: x / 2.54,

    "/miles_to_km": lambda x: x * 1.60934,
    "/km_to_miles": lambda x: x / 1.60934,

    "/pounds_to_kg": lambda x: x * 0.453592,
    "/kg_to_pounds": lambda x: x / 0.453592,

    "/fahrenheit_to_celsius": lambda x: (x - 32) * 5 / 9,
    "/celsius_to_fahrenheit": lambda x: (x * 9 / 5) + 32,

    "/ounces_to_ml": lambda x: x * 29.5735,
    "/ml_to_ounces": lambda x: x / 29.5735,

    "/gallons_to_liters": lambda x: x * 3.78541,
    "/liters_to_gallons": lambda x: x / 3.78541,

    "/feet_to_meters": lambda x: x * 0.3048,
    "/meters_to_feet": lambda x: x / 0.3048,

    "/yards_to_meters": lambda x: x * 0.9144,
    "/meters_to_yards": lambda x: x / 0.9144,

    "/cups_to_liters": lambda x: x * 0.236588,
    "/liters_to_cups": lambda x: x / 0.236588,
}


# Create a keyboard for the conversion menu
def create_keyboard(commands):
    buttons_row_1 = [
        InlineKeyboardButton(text="INCHES", callback_data="/inches_to_cm"),
        InlineKeyboardButton(text="MILES", callback_data="/miles_to_km"),
        InlineKeyboardButton(text="POUNDS", callback_data="/pounds_to_kg"),
    ]
    buttons_row_2 = [
        InlineKeyboardButton(text="F°", callback_data="/fahrenheit_to_celsius"),
        InlineKeyboardButton(text="OUNCES", callback_data="/ounces_to_ml"),
        InlineKeyboardButton(text="GALLONS", callback_data="/gallons_to_liters"),
    ]
    buttons_row_3 = [
        InlineKeyboardButton(text="FEET", callback_data="/feet_to_meters"),
        InlineKeyboardButton(text="YARDS", callback_data="/yards_to_meters"),
        InlineKeyboardButton(text="CUPS", callback_data="/cups_to_liters"),
    ]
    return InlineKeyboardMarkup(inline_keyboard=[
        buttons_row_1,
        buttons_row_2,
        buttons_row_3,
    ])


# Handle the /converter command to display the conversion menu
@router.message(Command("converter", prefix="/!%"))
async def converter_menu(message: types.Message):
    keyboard = create_keyboard(list(conversion_functions.keys()))
    await message.reply("Choose a conversion:", reply_markup=keyboard)


# Define a variable to store the last conversion command
last_conversion_command = None


# Handle callback queries from the conversion menu
@router.callback_query()
async def handle_conversion_query(callback_query: types.CallbackQuery):
    global last_conversion_command
    last_conversion_command = callback_query.data
    await callback_query.message.answer("Please enter the value to convert for " + last_conversion_command + ":")


# Handle messages containing only numbers
@router.message(lambda message: message.text.strip().isdigit() and last_conversion_command is not None)
async def handle_numbers(message: types.Message):
    if last_conversion_command in conversion_functions:
        try:
            number = float(message.text)
            result = conversion_functions[last_conversion_command](number)
            await message.reply(f"The result is: {result}")
        except ValueError:
            await message.reply("Invalid input. Please enter a valid number.")
    else:
        await message.reply("Please enter a valid conversion command first.")
