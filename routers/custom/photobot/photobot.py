import asyncio
import io
import logging
import os
import tempfile
import random
from typing import Tuple

from io import BytesIO
import aiohttp
import cv2
import moviepy.editor as mp
import numpy as np
import requests
from PIL import Image
from PIL import ImageChops
from aiogram import Bot, types, Dispatcher, F
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile, BufferedInputFile
from aiogram.types import InputFile
from aiogram.types import KeyboardButton
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup
from dotenv import load_dotenv
from aiogram.types import CallbackQuery
from moviepy.video.io.VideoFileClip import VideoFileClip

from keyboards.inline_keyboards.actions_kb import build_actions_kb

bot_token = os.getenv('BOT_TOKEN')
deep_ai_key = os.getenv('DEEP_AI_TOKEN')

load_dotenv()

bot = Bot(token=bot_token)
dp = Dispatcher()

router = Router(name=__name__)

logger = logging.getLogger(__name__)


class InputFileBytes(InputFile):
    def __init__(self, file_data: bytes, filename: str):
        """
        Represents the contents of a file to be uploaded from bytes data.

        :param file_data: Bytes data of the file
        :param filename: Name of the file
        """
        super().__init__(filename=filename)
        self.file_data = file_data

    async def read(self, bot):
        """
        Implementation of the read method to yield bytes data of the file.
        """
        yield self.file_data


class AIfilters(StatesGroup):
    Maskings = State()
    Filterings = State()
    Framings = State()
    Rembg = State()


class AIFiltersPIL(StatesGroup):
    NegPil = State()
    Colorize = State()


# Define predefined colors
COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    # Add more colors as needed
}

# MEME BOX
MEME_COUNT = 24


@router.message(Command("memes", prefix="!/"))
async def give_random_meme(message: types.Message):
    folder_path = os.path.join(os.getcwd(), "routers", "custom", "photobot", "meme_box")
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    if not files:
        await message.reply("No memes found :(")
        return

    random_meme = random.choice(files)
    file_path = os.path.join(folder_path, random_meme)

    photo = FSInputFile(file_path)
    await message.reply_photo(photo, caption="Here you are")


@router.message(Command("actions", prefix="!/"))
async def send_actions_message_w_kb(message: types.Message):
    await message.answer(
        text="Your actions:",
        reply_markup=build_actions_kb(),
    )


# STICKER BOT
class StickerButtonText:
    COOL_SERVAL = "Cool serval"
    SERVAL_IN_SUNGLASSES = "Serval in sunglasses"
    SUNEUS = "SunEus"
    STREET = "Street"
    OASIS = "Oasis"
    OLEG_2 = "Oleg 2.0"
    SKIBIDI = "Skibidi"
    RED_SQUARE = "Red Square"
    BLACK_SQUARE = "Black Square"
    KITTENS = "Kittens"


async def send_sticker(chat_id, sticker_id):
    url = f'https://api.telegram.org/bot{bot_token}/sendSticker'
    params = {'chat_id': chat_id, 'sticker': sticker_id}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=params) as response:
            return await response.json()


@router.message(Command("sticker_kb", prefix="!/"))
async def send_keyboard_command(message: types.Message):
    markup = get_sticker_kb()
    await message.answer("Choose a sticker:", reply_markup=markup)


def get_sticker_kb() -> ReplyKeyboardMarkup:
    buttons_row_1 = [
        KeyboardButton(text=StickerButtonText.COOL_SERVAL),
        KeyboardButton(text=StickerButtonText.SERVAL_IN_SUNGLASSES),
        KeyboardButton(text=StickerButtonText.SUNEUS)
    ]
    buttons_row_2 = [
        KeyboardButton(text=StickerButtonText.STREET),
        KeyboardButton(text=StickerButtonText.OASIS),
        KeyboardButton(text=StickerButtonText.OLEG_2)
    ]
    buttons_row_3 = [
        KeyboardButton(
            text=StickerButtonText.SKIBIDI
        ),
        KeyboardButton(
            text=StickerButtonText.RED_SQUARE),
        KeyboardButton(text=StickerButtonText.BLACK_SQUARE)
    ]
    buttons_row_4 = [
        KeyboardButton(text=StickerButtonText.KITTENS)
    ]

    markup_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            buttons_row_1,
            buttons_row_2,
            buttons_row_3,
            buttons_row_4
        ],
        resize_keyboard=True,
    )
    return markup_keyboard


async def process_button(callback_query: types.CallbackQuery, sticker_id: str):
    await callback_query.answer()
    await bot.send_sticker(callback_query.message.chat.id, sticker_id)


# 1
@router.callback_query(lambda query: query.data == 'cool_serv')
async def process_cool_serv(callback_query: types.CallbackQuery):
    await process_button(
        callback_query, 'CAACAgIAAxkBAT_slGXeebJxA-smlFeQFcexQR34-OsnAAKlRwACeIjxSufdBql9SW5PNAQ'
    )


@router.message(lambda message: message.text == StickerButtonText.COOL_SERVAL)
async def cool_serv_handler(message: types.Message):
    sticker_id = 'CAACAgIAAxkBAT_slGXeebJxA-smlFeQFcexQR34-OsnAAKlRwACeIjxSufdBql9SW5PNAQ'
    await send_sticker(message.chat.id, sticker_id)


# 2
@router.callback_query(lambda query: query.data == 'glasses_serv')
async def process_glasses_serv(callback_query: types.CallbackQuery):
    await process_button(
        callback_query, 'CAACAgIAAxkBAT_slmXeebWKjkaEg5xXdlFC9VJzFsSEAAJKSQAC4AfxSkws0ZUa6nFtNAQ'
    )


@router.message(lambda message: message.text == StickerButtonText.SERVAL_IN_SUNGLASSES)
async def sunglasses_serv_handler(message: types.Message):
    sticker_id = 'CAACAgIAAxkBAT_slmXeebWKjkaEg5xXdlFC9VJzFsSEAAJKSQAC4AfxSkws0ZUa6nFtNAQ'
    await send_sticker(message.chat.id, sticker_id)


# 3
@router.callback_query(lambda query: query.data == 'sun_eus')
async def process_cool_serv(callback_query: types.CallbackQuery):
    await process_button(
        callback_query, 'CAACAgIAAxkBAT_smGXeebe82JbxsqexupZWb9YOL2SaAALPRgACQ-_wSsms8aFXQhOSNAQ'
    )


@router.message(lambda message: message.text == StickerButtonText.SUNEUS)
async def sun_eus_handler(message: types.Message):
    sticker_id = 'CAACAgIAAxkBAT_smGXeebe82JbxsqexupZWb9YOL2SaAALPRgACQ-_wSsms8aFXQhOSNAQ'
    await send_sticker(message.chat.id, sticker_id)


# 4
@router.callback_query(lambda query: query.data == 'street')
async def process_glasses_serv(callback_query: types.CallbackQuery):
    await process_button(
        callback_query, 'CAACAgIAAxkBAT_soGXeebpSnYxCOPqUm4GiYDj15C6kAAK6RgACtanwSv8NkGfNOgS6NAQ'
    )


@router.message(lambda message: message.text == StickerButtonText.STREET)
async def street_handler(message: types.Message):
    sticker_id = 'CAACAgIAAxkBAT_soGXeebpSnYxCOPqUm4GiYDj15C6kAAK6RgACtanwSv8NkGfNOgS6NAQ'
    await send_sticker(message.chat.id, sticker_id)


# 5
@router.callback_query(lambda query: query.data == 'oasis')
async def process_cool_serv(callback_query: types.CallbackQuery):
    await process_button(
        callback_query, 'CAACAgIAAxkBAT_somXeebtdpovxM2aAqPEvW8ZCfyj4AAL8SwACY5rwSo_kEFHCOdpoNAQ'
    )


@router.message(lambda message: message.text == StickerButtonText.OASIS)
async def oasis_handler(message: types.Message):
    sticker_id = 'CAACAgIAAxkBAT_somXeebtdpovxM2aAqPEvW8ZCfyj4AAL8SwACY5rwSo_kEFHCOdpoNAQ'
    await send_sticker(message.chat.id, sticker_id)


# 6
@router.callback_query(lambda query: query.data == 'oleg')
async def process_glasses_serv(callback_query: types.CallbackQuery):
    await process_button(
        callback_query, 'CAACAgIAAxkBAT_spGXeebxGlwkUwCehdE1ugbducK6jAAJaTwACmqLxSiv44wKDZl_GNAQ'
    )


@router.message(lambda message: message.text == StickerButtonText.OLEG_2)
async def oleg_handler(message: types.Message):
    sticker_id = 'CAACAgIAAxkBAT_spGXeebxGlwkUwCehdE1ugbducK6jAAJaTwACmqLxSiv44wKDZl_GNAQ'
    await send_sticker(message.chat.id, sticker_id)


# 7
@router.callback_query(lambda query: query.data == 'toilet')
async def process_cool_serv(callback_query: types.CallbackQuery):
    await process_button(
        callback_query, 'CAACAgIAAxkBAT_smmXeebj_VnSxhZD20G1RNCOJ2gmeAAKdOgAC25D4SuqOAAFAo4NcKTQE'
    )


@router.message(lambda message: message.text == StickerButtonText.SKIBIDI)
async def skibidi_handler(message: types.Message):
    sticker_id = 'CAACAgIAAxkBAT_smmXeebj_VnSxhZD20G1RNCOJ2gmeAAKdOgAC25D4SuqOAAFAo4NcKTQE'
    await send_sticker(message.chat.id, sticker_id)


# 8
@router.callback_query(lambda query: query.data == 'red_square')
async def process_glasses_serv(callback_query: types.CallbackQuery):
    await process_button(
        callback_query, 'CAACAgIAAxkBAT_snGXeebkIeZvNweKIlzAG17XQbB1IAAKIRQACnfbwStsTyclJ3JsGNAQ'
    )


@router.message(lambda message: message.text == StickerButtonText.RED_SQUARE)
async def red_square_handler(message: types.Message):
    sticker_id = 'CAACAgIAAxkBAT_snGXeebkIeZvNweKIlzAG17XQbB1IAAKIRQACnfbwStsTyclJ3JsGNAQ'
    await send_sticker(message.chat.id, sticker_id)


# 9
@router.callback_query(lambda query: query.data == 'black_square')
async def process_cool_serv(callback_query: types.CallbackQuery):
    await process_button(
        callback_query, 'CAACAgIAAxkBAT_snmXeebqfEeJu5Sdzssod8rjLWCFdAAI3RQACMcvxSlyQjDvlecR5NAQ'
    )


@router.message(lambda message: message.text == StickerButtonText.BLACK_SQUARE)
async def black_square_handler(message: types.Message):
    sticker_id = 'CAACAgIAAxkBAT_snmXeebqfEeJu5Sdzssod8rjLWCFdAAI3RQACMcvxSlyQjDvlecR5NAQ'
    await send_sticker(message.chat.id, sticker_id)


# 10
@router.callback_query(lambda query: query.data == 'kittens')
async def process_glasses_serv(callback_query: types.CallbackQuery):
    await process_button(
        callback_query, 'CAACAgIAAxkBAT_q_mXeZb3RFKlAR4yp5GbS0nfsH0kbAAL9PQACIgzxSsCa0NR6qOSDNAQ'
    )


@router.message(lambda message: message.text == StickerButtonText.KITTENS)
async def kittens_handler(message: types.Message):
    sticker_id = 'CAACAgIAAxkBAT_q_mXeZb3RFKlAR4yp5GbS0nfsH0kbAAL9PQACIgzxSsCa0NR6qOSDNAQ'
    await send_sticker(message.chat.id, sticker_id)


# ======================================================================================================================
# You can add presentations into the 'presentations' folder of PhotoBot
@router.message(Command("presentation", prefix="!/"))
async def send_presentation(message: types.Message):
    presentations_dir = os.path.join(os.path.dirname(__file__), "presentations")

    if not os.path.exists(presentations_dir):
        await message.answer("Sorry, the presentations are not available at the moment.")
        return

    presentations = [f for f in os.listdir(presentations_dir) if f.endswith('.pptx')]

    if not presentations:
        await message.answer("Sorry, there are no presentations available at the moment.")
        return

    presentation_path = os.path.join(presentations_dir, presentations[0])

    # Send the presentation using types.InputFile
    await message.answer_document(types.FSInputFile(presentation_path, presentations[0]))


# DEEP AI ==============================================================================================================
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = 'deep_ai_txt.txt'
FILE_PATH = os.path.join(CURRENT_DIRECTORY, FILE_NAME)


# Function to generate an image from text using DeepAI API
async def generate_image_from_text(text: str, deep_ai_key: str) -> str:
    try:
        response = requests.post(
            "https://api.deepai.org/api/text2img",
            data={'text': text},
            headers={'api-key': deep_ai_key}
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_json = response.json()
        output_url = response_json.get("output_url")
        if output_url:
            return output_url
        else:
            return "Sorry, I couldn't generate an image at the moment."
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


# Handler for the /photo_deep_ai command
@router.message(Command("photo_deep_ai", prefix="!/"))
async def ask_photo_gpt_deep_ai(message: Message):
    deep_ai_key = os.getenv('DEEP_AI_KEY')
    if not deep_ai_key:
        await message.answer("DeepAI API key is not configured properly.")
        return

    print("File path:", FILE_PATH)  # Debug statement

    # Read text from the file
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as file:
            text = file.read()
            print("Text from file:", text)  # Debug statement
    except FileNotFoundError:
        await message.answer("Sorry, the text file is not found.")
        return
    except Exception as e:
        await message.answer(f"An error occurred while reading the file: {str(e)}")
        return

    # Generate image from text
    output_url = await generate_image_from_text(text, deep_ai_key)
    await message.answer_photo(output_url)


# Handler for the /ask_deep_ai command
@router.message(Command("ask_deep_ai", prefix="!/"))
async def start_photo_deep_ai(message: Message):
    await message.answer("Привет! Задайте ваш вопрос.")
    # Set the state if needed


# Handler for all other messages
# @router.message(AIfilters.Rembg)
# async def answer_photo_deep_ai(message: Message, state: FSMContext):
#     # Get the current state directly
#     current_state = await state.get_state()
#
#     if current_state == AIfilters.Filterings:
#         question = message.text
#         deep_ai_key = os.getenv('DEEP_AI_KEY')
#
#         if not deep_ai_key:
#             await message.answer("DeepAI API key is not configured properly.")
#             return
#
#         # Generate image from text
#         output_url = await generate_image_from_text(question, deep_ai_key)
#         await message.answer_photo(output_url)
#
#         # Clear the state if using FSM
#         await state.clear()

# REMOVE BACKGROUND ====================================================================================================
# Handler for the /rembg command to enter the Rembg state
# @router.message(Command("rembg", prefix="/"))
# async def start_removing_background(message: Message, state: FSMContext):
#     await message.answer("Please provide an image URL to remove the background.")
#     await state.set_state(AIfilters.Rembg)
#
#
# # Handler for processing photos
# @router.message(F.photo)
# async def handle_photo(message: Message, state: FSMContext):
#     # Check if the bot is in the Rembg state
#     if (await state.get_state()) != 'AIFilters:Rembg':
#         await message.answer("You need to use the /rembg command first.")
#         return
#
#     if not deep_ai_key:
#         await message.answer("DeepAI API key is not configured properly.")
#         return
#
#     # Extract the image URL from the message
#     if not message.photo:
#         await message.answer("Please provide a valid photo.")
#         return
#
#     photo_file_id = message.photo[-1].file_id
#     photo_url = f"https://api.telegram.org/file/bot{bot_token}/" \
#                 f"{(await bot.get_file(photo_file_id)).file_path}"
#
#     # Remove background from the image
#     output_url = await remove_background(photo_url, deep_ai_key)
#     await message.answer_photo(output_url)
#
# # Handler for the /remove_bg_deep_ai command
# @router.message(Command("remove_bg_deep_ai", prefix="!/"))
# async def remove_background_deep_ai(message: Message, state: FSMContext):
#     if not deep_ai_key:
#         await message.answer("DeepAI API key is not configured properly.")
#         return
#
#     # Check if the bot is in the Rembg state
#     if (await state.get_state()) != AIfilters.Rembg:
#         await message.answer("You need to use the /rembg command first.")
#         return
#
#     # Extract the image URL from the message
#     command_args = message.text.split(' ', 1)[1].strip()
#     if not command_args:
#         await message.answer("Please provide an image URL.")
#         return
#
#     # Remove background from the image
#     output_url = await remove_background(command_args, deep_ai_key)
#     await message.answer_photo(output_url)
#
# # Function to remove background from an image using DeepAI API
# async def remove_background(image_url: str, deep_ai_key: str) -> str:
#     try:
#         response = requests.post(
#             "https://api.deepai.org/api/background-remover",
#             data={'image': image_url},
#             headers={'api-key': deep_ai_key}
#         )
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         response_json = response.json()
#         output_url = response_json.get("output_url")
#         if output_url:
#             return output_url
#         else:
#             return "Sorry, I couldn't remove the background at the moment."
#     except requests.exceptions.RequestException as e:
#         return f"Error: {e}"

# COLORIZER ============================================================================================================
# Function to colorize black and white images using DeepAI API
# async def colorize_image(image_url: str, deep_ai_key: str) -> str:
#     try:
#         response = requests.post(
#             "https://api.deepai.org/api/colorizer",
#             data={'image': image_url},
#             headers={'api-key': deep_ai_key}
#         )
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         response_json = response.json()
#         output_url = response_json.get("output_url")
#         if output_url:
#             return output_url
#         else:
#             return "Sorry, I couldn't colorize the image at the moment."
#     except requests.exceptions.RequestException as e:
#         return f"Error: {e}"
#
# # Handler for the /colorize_image_deep_ai command
# @router.message(Command("colorize_image_deep_ai", prefix="!/"))
# async def colorize_image_deep_ai(message: Message):
#     deep_ai_key = os.getenv('DEEP_AI_KEY')
#     if not deep_ai_key:
#         await message.answer("DeepAI API key is not configured properly.")
#         return
#
#     # Extract the image URL from the message
#     image_url = message.get_args()
#     if not image_url:
#         await message.answer("Please provide an image URL.")
#         return
#
#     # Colorize the image
#     output_url = await colorize_image(image_url, deep_ai_key)
#     await message.answer_photo(output_url)

# IMAGE FROM TEXT ======================================================================================================
# Function to generate an image from text using DeepAI API
# async def generate_image_from_text(text: str, deep_ai_key: str) -> str:
#     try:
#         response = requests.post(
#             "https://api.deepai.org/api/text2img",
#             data={'text': text},
#             headers={'api-key': deep_ai_key}
#         )
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         response_json = response.json()
#         output_url = response_json.get("output_url")
#         if output_url:
#             return output_url
#         else:
#             return "Sorry, I couldn't generate an image at the moment."
#     except requests.exceptions.RequestException as e:
#         return f"Error: {e}"
#
# # Handler for the /generate_image_deep_ai command
# @router.message(Command("generate_image_deep_ai", prefix="!/"))
# async def generate_image_deep_ai(message: Message):
#     deep_ai_key = os.getenv('DEEP_AI_KEY')
#     if not deep_ai_key:
#         await message.answer("DeepAI API key is not configured properly.")
#         return
#
#     # Extract the text description from the message
#     text = message.get_args()
#     if not text:
#         await message.answer("Please provide a text description.")
#         return
#
#     # Generate image from text
#     output_url = await generate_image_from_text(text, deep_ai_key)
#     await message.answer_photo(output_url)

# AI Image Editor ======================================================================================================
# Function to edit an image using AI Image Editor from DeepAI API
# async def edit_image_with_ai(image_url: str, text: str, deep_ai_key: str) -> str:
#     try:
#         response = requests.post(
#             "https://api.deepai.org/api/image-editor",
#             data={'image': image_url, 'text': text},
#             headers={'api-key': deep_ai_key}
#         )
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         response_json = response.json()
#         output_url = response_json.get("output_url")
#         if output_url:
#             return output_url
#         else:
#             return "Sorry, I couldn't edit the image at the moment."
#     except requests.exceptions.RequestException as e:
#         return f"Error: {e}"
#
# # Handler for the /edit_image_deep_ai command
# @router.message(Command("edit_image_deep_ai", prefix="!/"))
# async def edit_image_deep_ai(message: Message):
#     deep_ai_key = os.getenv('DEEP_AI_KEY')
#     if not deep_ai_key:
#         await message.answer("DeepAI API key is not configured properly.")
#         return
#
#     # Extract the image URL and text from the message
#     args = message.get_args().split()
#     if len(args) != 2:
#         await message.answer("Please provide an image URL and text.")
#         return
#     image_url, text = args
#
#     # Edit the image using AI Image Editor
#     output_url = await edit_image_with_ai(image_url, text, deep_ai_key)
#     await message.answer_photo(output_url)

# Super Resolution =====================================================================================================
# Function to apply Super Resolution to an image using DeepAI API
# async def apply_super_resolution(image_url: str, deep_ai_key: str) -> str:
#     try:
#         response = requests.post(
#             "https://api.deepai.org/api/torch-srgan",
#             data={'image': image_url},
#             headers={'api-key': deep_ai_key}
#         )
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         response_json = response.json()
#         output_url = response_json.get("output_url")
#         if output_url:
#             return output_url
#         else:
#             return "Sorry, I couldn't apply Super Resolution to the image at the moment."
#     except requests.exceptions.RequestException as e:
#         return f"Error: {e}"
#
# # Handler for the /super_resolution command
# @router.message(Command("super_resolution", prefix="!/"))
# async def super_resolution(message: Message):
#     deep_ai_key = os.getenv('DEEP_AI_KEY')
#     if not deep_ai_key:
#         await message.answer("DeepAI API key is not configured properly.")
#         return
#
#     # Extract the image URL from the message
#     image_url = message.get_args()
#
#     # Apply Super Resolution to the image
#     output_url = await apply_super_resolution(image_url, deep_ai_key)
#     await message.answer_photo(output_url)

# Waifu2x ==============================================================================================================
# '''
# Extract the photo URL or file ID from the message.
# Pass the URL or file ID to the appropriate function for processing.
# Process the photo using the DeepAI API or any other image processing API.
# Send the processed result back to the user.
# '''
# # Function to apply Waifu2x to an image using DeepAI API
# # Define states for handling the photo upload process
# UPLOADS_DIR = 'photos'
#
#
# class Waifu2xState(StatesGroup):
#     uploading_photo = State()
#
#
# # Function to apply Waifu2x to an image using DeepAI API
# async def apply_waifu2x(image_data: bytes, deep_ai_key: str) -> str:
#     try:
#         response = requests.post(
#             "https://api.deepai.org/api/waifu2x",
#             files={'image': image_data},
#             headers={'api-key': deep_ai_key}
#         )
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         response_json = response.json()
#         output_url = response_json.get("output_url")
#         if output_url:
#             return output_url
#         else:
#             return "Sorry, I couldn't apply Waifu2x to the image at the moment."
#     except requests.exceptions.RequestException as e:
#         return f"Error: {e}"
#
#
# # Handler for the /waifu2x command
# @router.message(Command("waifu2x", prefix="!/"))
# async def waifu2x_command(message: Message, state: FSMContext):
#     # Ask the user to upload a photo
#     await message.answer("Please upload a photo >w^")
#
#     # Set the state to indicate that we are expecting a photo upload
#     await state.set_state(Waifu2xState.uploading_photo)
#
#
# # Handler for handling the uploaded photo
# @router.message(F.photo, Waifu2xState.uploading_photo)  # HOW TO HANDLE PHOTOS?
# async def handle_uploaded_photo(message: types.Message, state: FSMContext):
#     deep_ai_key = os.getenv('DEEP_AI_TOKEN')
#     if not deep_ai_key:
#         await message.answer("DeepAI API key is not configured properly.")
#         return
#
#     # Get the file ID of the uploaded photo
#     file_id = message.photo[-1].file_id
#
#     try:
#         # Download the file to the uploads directory
#         downloaded_file_path = await message.bot.download(file_id, destination=UPLOADS_DIR)
#
#         # Read the file content
#         async with aiofiles.open(downloaded_file_path, 'rb') as file:
#             photo_data = await file.read()
#
#         # Apply Waifu2x to the photo
#         output_url = await apply_waifu2x(photo_data, deep_ai_key)
#
#         # Send the processed photo back to the user
#         await message.answer_photo(output_url)
#
#     except (aiogram.exceptions.TelegramAPIError, PermissionError):
#         await message.answer("Failed to download or process the photo.")
#
#     # Reset the state
#     await state.clear()


# PILLOW INVERSION =====================================================================================================
# # Handler for the /rembg command to enter the Rembg state
# @router.message(Command("rembg_pil", prefix="/"))
# async def start_removing_background_pil(message: types.Message, state: FSMContext):
#     await message.answer("Please send the photo to remove its background.")
#     await state.set_state(AIFiltersPIL.NegPil)
#
#
# # Handler for processing photos
# @router.message(F.photo)
# async def handle_photo_pil(message: types.Message, state: FSMContext):
#     await state.set_state(AIFiltersPIL.NegPil)
#     try:
#         # Get the file ID of the largest available photo
#         file_id = message.photo[-1].file_id
#
#         # Download the photo file data
#         file_path = (await message.bot.get_file(file_id)).file_path
#         photo_data_stream = await message.bot.download_file(file_path)
#
#         # Read the bytes data from the stream
#         photo_data = photo_data_stream.read()
#
#         # Process the photo to remove the background
#         processed_photo_data = await process_photo(photo_data)
#
#         # Convert the processed photo data to an InputFile object
#         processed_photo_input_file = InputFileBytes(processed_photo_data, filename="processed_photo.png")
#
#         # Send the processed photo back to the user
#         await message.answer_photo(processed_photo_input_file)
#
#         # Reset state
#         await state.clear()
#     except Exception as e:
#         logger.exception("Failed to process photo:", exc_info=e)
#         await message.answer("Failed to process the photo. Please try again later.")
#
#
# async def process_photo(photo_data: bytes) -> bytes:
#     try:
#         # Convert the byte data into a numpy array
#         nparr = np.frombuffer(photo_data, np.uint8)
#
#         # Decode the numpy array into an OpenCV image
#         image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#
#         # Convert the image to grayscale
#         grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#         # Apply thresholding to segment the foreground from the background
#         _, thresholded_img = cv2.threshold(grayscale_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#
#         # Invert the thresholded image
#         inverted_img = cv2.bitwise_not(thresholded_img)
#
#         # Convert the inverted image back to bytes
#         _, processed_photo_data = cv2.imencode('.png', inverted_img)
#
#         return processed_photo_data.tobytes()
#     except Exception as e:
#         logger.exception("Failed to process photo:", exc_info=e)
#         raise

# PILLOW COLORIZER  ====================================================================================================
async def process_photo(photo_data: bytes, color_filter: Tuple[int, int, int] = None) -> bytes:
    try:
        # Convert the byte data into a numpy array
        nparr = np.frombuffer(photo_data, np.uint8)

        # Decode the numpy array into an OpenCV image
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if color_filter is not None:
            # Convert the image to float32 data type
            image = image.astype(np.float32)

            # Normalize the color filter values to the range [0, 1]
            color_filter = np.array(color_filter, dtype=np.float32) / 255.0

            # Reshape the color filter to a single-row matrix
            color_filter = color_filter.reshape(1, 3)

            # Apply a color filter to the image
            colored_image = cv2.add(image, color_filter)

            # Clip values to ensure they are within the valid range
            colored_image = np.clip(colored_image, 0, 255)

            # Convert the colored image back to bytes
            _, processed_photo_data = cv2.imencode('.png', colored_image.astype(np.uint8))
        else:
            # Convert the image to grayscale
            grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply thresholding to segment the foreground from the background
            _, thresholded_img = cv2.threshold(grayscale_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Invert the thresholded image
            inverted_img = cv2.bitwise_not(thresholded_img)

            # Convert the inverted image back to bytes
            _, processed_photo_data = cv2.imencode('.png', inverted_img)

        return processed_photo_data.tobytes()
    except Exception as e:
        logger.exception("Failed to process photo:", exc_info=e)
        raise


@router.message(Command("negative", prefix="/"))
async def start_negative_pil(message: types.Message, state: FSMContext):
    await message.answer("Please send the photo to revert colors.")
    await state.set_state(AIFiltersPIL.NegPil)


@router.message(Command("colorize", prefix="/"))
async def start_colorizing_pil(message: types.Message, state: FSMContext):
    await message.answer("Please send the photo to colorize.")
    await state.set_state(AIFiltersPIL.Colorize)


# Handler for processing photos during negative process
@router.message(AIFiltersPIL.NegPil, F.photo)
async def handle_photo_negative(message: types.Message, state: FSMContext):
    try:
        # Get the file ID of the largest available photo
        file_id = message.photo[-1].file_id

        # Download the photo file data
        file_path = (await message.bot.get_file(file_id)).file_path
        photo_data_stream = await message.bot.download_file(file_path)

        # Read the bytes data from the stream
        photo_data = photo_data_stream.read()

        processed_photo_data = await process_photo(photo_data)

        # Convert the processed photo data to an InputFile object
        processed_photo_input_file = InputFileBytes(processed_photo_data, filename="processed_photo.png")

        # Send the processed photo back to the user
        await message.answer_photo(processed_photo_input_file)

        # Reset state
        await state.clear()
    except Exception as e:
        logger.exception("Failed to process photo:", exc_info=e)
        await message.answer("Failed to process the photo. Please try again later.")


# Handler for processing photos during colorizing process
@router.message(AIFiltersPIL.Colorize, F.photo)
async def handle_photo_colorization(message: types.Message, state: FSMContext):
    try:
        # Get the file ID of the largest available photo
        file_id = message.photo[-1].file_id

        # Download the photo file data
        file_path = (await message.bot.get_file(file_id)).file_path
        photo_data_stream = await message.bot.download_file(file_path)

        # Prompt the user to select a color
        color_message = "Please select a color for colorization:\n"

        # Create the reply keyboard markup with resize_keyboard=True
        color_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

        # Create a list of KeyboardButton instances for each color name
        for color_name in COLORS:
            button = KeyboardButton(text=color_name.capitalize())
            color_keyboard.add(button)

        # Add the keyboard field to the reply keyboard markup
        color_keyboard_data = color_keyboard.dict()

        # Add the keyboard field to the reply keyboard markup
        color_keyboard_data['keyboard'] = []

        await message.answer(color_message, reply_markup=color_keyboard)

        # Wait for the user's response (color name)
        response = await message.bot.wait_for(types.ContentTypes.TEXT, state=AIFiltersPIL.Colorize)

        # Parse the user's input to get the color
        color_name = response.text.strip().lower()
        color = COLORS.get(color_name)

        if not color:
            await message.answer("Invalid color name. Please try again.")
            return

        with Image.open(photo_data_stream) as image:
            # Colorize the image using the specified color
            colorized_image = colorize_image_pil(image, color)

            # Convert the colorized image to bytes
            with io.BytesIO() as buffer:
                colorized_image.save(buffer, format="PNG")
                colorized_image_data = buffer.getvalue()

            # Send the colorized image back to the user
            await message.answer_photo(InputFile(colorized_image_data))

        # Reset state
        await state.clear()
    except Exception as e:
        logger.exception("Failed to process photo:", exc_info=e)
        await message.answer("Failed to process the photo. Please try again later.")


async def colorize_image_pil(image: Image.Image, color: Tuple[int, int, int]) -> Image.Image:
    """
    Colorize the input image with the specified color using PIL.

    :param image: PIL Image object
    :param color: Color to apply to the image, specified as an RGB tuple (e.g., (255, 0, 0) for red)
    :return: Colorized image object
    """
    try:
        # Convert the image to RGB mode if it's not already in that mode
        image = image.convert("RGB")

        # Create a solid color overlay image
        overlay = Image.new("RGB", image.size, color)

        # Convert the overlay to grayscale
        overlay_gray = overlay.convert("L")

        # Blend the original image with the grayscale version of the color overlay using the "multiply" blending mode
        colorized_image = ImageChops.multiply(image, overlay_gray)

        return colorized_image
    except Exception as e:
        logger.exception("Failed to colorize image:", exc_info=e)
        raise


# VIDEO TO MP3 CONVERTER ===============================================================================================
class VideoMaster(StatesGroup):
    WaitingForVideo = State()

@router.message(F.video)
async def handle_video(message: Message, state: FSMContext):
    await state.set_state(VideoMaster.WaitingForVideo)
    if message.video.duration <= 30:
        video_file = await message.bot.get_file(message.video.file_id)

        # Download the video file into memory
        input_video_stream = BytesIO()
        await message.bot.download_file(video_file.file_path, destination=input_video_stream)

        # Write the video stream to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video_file:
            temp_video_file.write(input_video_stream.getvalue())
            temp_video_file_path = temp_video_file.name

        # Extract audio from the video
        video = VideoFileClip(temp_video_file_path)
        temp_audio_file_path = temp_video_file_path.replace(".mp4", ".mp3")
        video.audio.write_audiofile(temp_audio_file_path)
        video.close()  # Close the VideoFileClip instance

        # Open the audio file and send it as a voice message
        with open(temp_audio_file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            audio = BufferedInputFile(audio_bytes, filename="audio.mp3")
            await message.reply_document(audio)
            # await message.reply_voice(audio) for voice messages

        # Remove the temporary files
        os.unlink(temp_video_file_path)
        os.unlink(temp_audio_file_path)

        await state.clear()
    else:
        await message.answer("Sorry, the video duration exceeds the limit of 30 seconds.")

@router.message(Command("video_to_mp3", prefix="!/"))
async def start_video(message: Message, state: FSMContext):
    await state.set_state(VideoMaster.WaitingForVideo)
    await message.answer("Send me a video (30 seconds maximum).")
