import os

from aiogram import Bot
from aiogram import Router
from aiogram import types, Dispatcher
from aiogram.filters import Command
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
