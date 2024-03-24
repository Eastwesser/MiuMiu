import csv
import io
import os
import re

import aiohttp
from aiogram import Bot
from aiogram import Router, F
from aiogram import types, Dispatcher
from aiogram.enums import ParseMode, ChatAction
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils import markdown
from aiogram.utils.chat_action import ChatActionSender
from dotenv import load_dotenv

from keyboards.inline_keyboards.miumiu_kb import build_miumiu_kb
from keyboards.inline_keyboards.shop_kb import build_shop_kb
from keyboards.inline_keyboards.simple_row import make_row_keyboard

bot_token = os.getenv('BOT_TOKEN')
forecast_api = os.getenv('WEATHER_API_TOKEN')
load_dotenv()

bot = Bot(token=bot_token)
dp = Dispatcher()

router = Router(name=__name__)


@router.message(Command("code", prefix="/!%"))
async def handle_command_code(message: types.Message):
    text = markdown.text(
        "Here's Python code:",
        "",
        markdown.markdown_decoration.pre_language(
            markdown.text("def is_palindrome(word):",
                          "    # Remove spaces and convert to lowercase",
                          "    word = word.lower().replace(' ', '')",
                          "    # Check if the string is a palindrome",
                          "    return word == word[::-1]",
                          "",
                          "# Example usage:",
                          'word = "level"',
                          "print(is_palindrome(word))  # Output: True",
                          sep="\n",
                          ),
            language="python",
        ),
        "And here's some JS:",
        "",
        markdown.markdown_decoration.pre_language(
            markdown.text('function isPalindrome(word) {',
                          '    // Remove spaces and convert to lowercase',
                          '    word = word.toLowerCase().replace(" ", "");',
                          '    // Check if the string is a palindrome',
                          '    return word === word.split("").reverse().join("");',
                          '}',
                          '',
                          '// Example usage:',
                          'let word = "level";',
                          'console.log(isPalindrome(word)); // Output: True',
                          sep="\n",
                          ),
            language="javascript",
        ),
        sep="\n",
    )
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)


@router.message(Command("pic"))
async def handle_command_pic(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_PHOTO,
    )
    url = "https://t4.ftcdn.net/jpg/00/97/58/97/360_F_97589769_t45CqXyzjz0KXwoBZT9PRaWGHRk5hQqQ.jpg"

    await message.reply_photo(
        photo=url,
    )


@router.message(Command("file"))
async def handle_command_file(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    file_path = "/Users/altte/cats/cat1.jpg"  # your path to file C:\Users\altte\cats and cat1, cat2, cat3
    await message.reply_document(
        document=types.FSInputFile(
            path=file_path,
            filename="cute-kitten.jpg",
        ),
    )


@router.message(Command("love", prefix="!/"))
async def handle_command_file(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    file_path = "/Users/altte/cats/cat4.png"  # your path to file C:\Users\altte\cats and cat1, cat2, cat3
    await message.reply_document(
        document=types.FSInputFile(
            path=file_path,
            filename="cute-kitten-love.png",
        ),
    )


@router.message(Command("text", prefix="!/"))
async def send_txt_file(message: types.Message):
    file = io.StringIO()
    file.write("Hello, world!\n")
    file.write("This is a text file.\n")
    await message.reply_document(
        document=types.BufferedInputFile(
            file=file.getvalue().encode("utf-8"),
            filename="text.txt",
        ),
    )


@router.message(Command("csv"))
async def send_csv_file(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    file = io.StringIO()
    csv_writer = csv.writer(file)
    csv_writer.writerows(
        [
            ["Name", "Age", "City"],
            ["Dennis Mattews", "28", "Moscow"],
            ["Diona Mattews", "2", "St.Petersburg"],
            ["Veronika Mattews", "26", "Moscow"],
        ]
    )
    await message.reply_document(
        document=types.BufferedInputFile(
            file=file.getvalue().encode("utf-8"),
            filename="people.csv",
        ),
    )


async def send_big_file(message: types.Message):
    # await asyncio.sleep(7)
    file = io.BytesIO()
    url = "https://images.unsplash.com/photo-1608848461950-0fe51dfc41cb"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result_bytes = await response.read()

    file.write(result_bytes)
    await message.reply_document(
        document=types.BufferedInputFile(
            file=file.getvalue(),
            filename="cute-kitten.jpg",
        ),
    )


@router.message(Command("pic_file"))  # sends you a fat document with a cat
async def send_pic_file_buffered(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )

    async with ChatActionSender.upload_document(
            bot=message.bot,
            chat_id=message.chat.id,
    ):
        await send_big_file(message)


# SHOP COMMAND
@router.message(Command("shop", prefix="!/"))
async def send_shop_message_kb(message: types.Message):
    await message.answer(
        text="Your shop actions: ",
        reply_markup=build_shop_kb(),
    )


# MIUMIU COMMAND
@router.message(Command("miumiu", prefix="!/"))
async def send_shop_message_kb(message: types.Message):
    await message.answer(
        text="MiuMiu actions: ",
        reply_markup=build_miumiu_kb(),
    )


# TASTY FOOD SHOP ======================================================================================================
available_food_names = ["Суши", "Спагетти", "Хачапури"]
available_food_sizes = ["Маленькую", "Среднюю", "Большую"]
available_drink_names = ["Чай", "Кофе", "Сок"]

# Define a dictionary to store user data
user_data = {}

# Define states for the order process
class OrderFood(StatesGroup):
    choosing_food_name = State()
    choosing_food_size = State()


class OrderDrink(StatesGroup):
    choosing_drink_name = State()


class OrderEmailPhone(StatesGroup):
    awaiting_contact_info = State()


def calculate_total_price(chosen_food: str, chosen_drink: str = None) -> int:
    """
    Calculate the total price of the order based on the selected food and drink items.

    Args:
        chosen_food (str): The chosen food item.
        chosen_drink (str, optional): The chosen drink item. Defaults to None if no drink is chosen.

    Returns:
        int: The total price of the order.
    """
    # Define placeholder prices for food items
    food_prices = {
        "Суши": 300,
        "Спагетти": 250,
        "Хачапури": 200,
    }

    # Define placeholder prices for drink items
    drink_prices = {
        "Чай": 100,
        "Кофе": 150,
        "Сок": 120,
    }

    total_price = food_prices.get(chosen_food, 0)  # Get the price of the chosen food item, default to 0 if not found

    # Add the price of the chosen drink item if any
    if chosen_drink:
        total_price += drink_prices.get(chosen_drink, 0)

    return total_price


# Define functions to validate email and phone number
def validate_email(email: str) -> bool:
    # Split the email by "@"
    parts = email.split("@")

    # Check if there are exactly two parts
    if len(parts) != 2:
        return False

    # Check if both parts have content
    if not parts[0] or not parts[1]:
        return False

    # Check if there are more than one "@" symbol
    if "@" in parts[1][1:]:
        return False

    # Check if there are any invalid characters in domain part
    invalid_chars = set("!#$%^&*()=+{}[]|;:,<>")
    if any(char in invalid_chars for char in parts[1]):
        return False

    # Check if the domain part has at least one dot
    if "." not in parts[1]:
        return False

    # Check if the email has at least one character before and after "@"
    if not parts[0] or not parts[1]:
        return False

    return True


def validate_phone(phone: str) -> bool:
    # Define the regex pattern for the phone number format
    pattern = r'^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$'

    # Use re.match to check if the phone number matches the pattern
    if re.match(pattern, phone):
        return True
    else:
        return False


@router.message(Command("food"))
async def cmd_food(message: Message):
    await message.answer(
        text="Выберите блюдо:",
        reply_markup=make_row_keyboard(available_food_names)
    )


@router.message(F.text.in_(available_food_names))
async def food_chosen(message: Message):
    chosen_food = message.text.lower()
    user_data['chosen_food'] = chosen_food
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите размер порции:",
        reply_markup=make_row_keyboard(available_food_sizes)
    )


@router.message(F.text.in_(available_food_sizes))
async def food_size_chosen(message: Message):
    chosen_food_size = message.text.lower()
    chosen_food = user_data.get('chosen_food')
    await message.answer(
        text=f"Вы выбрали {chosen_food_size} порцию {chosen_food}.\n"
             f"Попробуйте теперь заказать напитки: /drinks",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command("drinks"))
async def cmd_drinks(message: Message):
    await message.answer(
        text="Выберите напиток:",
        reply_markup=make_row_keyboard(available_drink_names)
    )


@router.message(F.text.in_(available_drink_names))
async def drink_chosen(message: Message):
    chosen_drink = message.text.lower()
    user_data['chosen_drink'] = chosen_drink
    await message.answer(
        text="Спасибо. Что-нибудь еще?",
        reply_markup=make_row_keyboard(["Добавить порцию", "Да, всё"])
    )


@router.message(F.text.isin(["Добавить порцию", "Да, всё"]))
async def anything_else(message: Message):
    choice = message.text
    if choice == "Добавить порцию":
        await message.answer(
            text="Выберите блюдо:",
            reply_markup=make_row_keyboard(available_food_names)
        )
    else:
        total_price = calculate_total_price(user_data["chosen_food"], user_data.get("chosen_drink"))
        await message.answer(
            text=f"Ваш заказ:\n\n"
                 f"- Блюдо: {user_data['chosen_food']}\n"
                 f"- Напиток: {user_data.get('chosen_drink', 'Нет')}\n"
                 f"Общая стоимость: {total_price} руб.\n\n"
                 "Введите ваше имя и фамилию, адрес электронной почты и номер телефона для связи:"
        )


@router.message
async def handle_message(message: Message):
    await message.answer(
        text="Выберите напиток или продолжите оформление заказа:"
    )
