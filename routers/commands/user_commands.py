import csv
import io
import os

import aiohttp
from aiogram import Bot
from aiogram import Router, F
from aiogram import types, Dispatcher
from aiogram.enums import ParseMode, ChatAction
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
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


# TASTY FOOD SHOP
available_food_names = ["Суши", "Спагетти", "Хачапури"]
available_food_sizes = ["Маленькую", "Среднюю", "Большую"]


class OrderFood(StatesGroup):
    choosing_food_name = State()
    choosing_food_size = State()


@router.message(Command("food"))
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите блюдо:",
        reply_markup=make_row_keyboard(available_food_names)
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(OrderFood.choosing_food_name)


@router.message(OrderFood.choosing_food_name, F.text.in_(available_food_names))
async def food_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_food=message.text.lower())
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите размер порции:",
        reply_markup=make_row_keyboard(available_food_sizes)
    )
    await state.set_state(OrderFood.choosing_food_size)


@router.message(StateFilter("OrderFood:choosing_food_name"))
async def food_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого блюда.\n\n"
             "Пожалуйста, выберите одно из названий из списка ниже:",
        reply_markup=make_row_keyboard(available_food_names)
    )


@router.message(OrderFood.choosing_food_size, F.text.in_(available_food_sizes))
async def food_size_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали {message.text.lower()} порцию {user_data['chosen_food']}.\n"
             f"Попробуйте теперь заказать напитки: /drinks",
        reply_markup=ReplyKeyboardRemove()
    )
    # Сброс состояния и сохранённых данных у пользователя
    await state.clear()


@router.message(OrderFood.choosing_food_size)
async def food_size_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого размера порции.\n\n"
             "Пожалуйста, выберите один из вариантов из списка ниже:",
        reply_markup=make_row_keyboard(available_food_sizes)
    )
