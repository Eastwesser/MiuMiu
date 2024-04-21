import base64
import json
import logging
import os
import random
import tempfile
import time
from io import BytesIO

import aiohttp
import cv2
import numpy as np
import requests
from aiogram import Bot, types, Dispatcher, F
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile, BufferedInputFile
from aiogram.types import InputFile
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
from moviepy.video.io.VideoFileClip import VideoFileClip

from keyboards.inline_keyboards.actions_kb import build_actions_kb

bot_token = os.getenv('BOT_TOKEN')
fusion_brain_token = os.getenv('FUSION_BRAIN_TOKEN')
fusion_brain_key = os.getenv('FB_KEY')

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


# PowerPoint Presentation ==============================================================================================
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


# PILLOW INVERSION =====================================================================================================
@router.message(Command("invert", prefix="/"))
async def start_inverting_colors_pil(message: types.Message, state: FSMContext):
    await message.answer("Please send the photo to invert the colors.")
    await state.set_state(AIFiltersPIL.NegPil)


@router.message(F.photo)
async def handle_photo_pil(message: types.Message, state: FSMContext):
    await state.set_state(AIFiltersPIL.NegPil)
    try:
        # Get the file ID of the largest available photo
        file_id = message.photo[-1].file_id

        # Download the photo file data
        file_path = (await message.bot.get_file(file_id)).file_path
        photo_data_stream = await message.bot.download_file(file_path)

        # Read the bytes data from the stream
        photo_data = photo_data_stream.read()

        # Process the photo to remove the background
        processed_photo_data = await process_photo_inversion(photo_data)

        # Convert the processed photo data to an InputFile object
        processed_photo_input_file = InputFileBytes(processed_photo_data, filename="processed_photo.png")

        # Send the processed photo back to the user
        await message.answer_photo(processed_photo_input_file)

        # Reset state
        await state.clear()

    except Exception as e:
        logger.exception("Failed to process photo:", exc_info=e)
        await message.answer("Failed to process the photo. Please try again later.")


async def process_photo_inversion(photo_data: bytes) -> bytes:
    try:
        # Convert the byte data into a numpy array
        nparr = np.frombuffer(photo_data, np.uint8)

        # Decode the numpy array into an OpenCV image
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

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


# KADINSKIY ============================================================================================================
class KadinskyStates(StatesGroup):
    Intro = State()
    TextToImage = State()


class ButtonTextKadinsky:
    TEXT_TO_IMAGE = "Text to image"


API_URL = "https://api-key.fusionbrain.ai/"

MODELS_ENDPOINT = API_URL + "key/api/v1/models"
GENERATE_ENDPOINT = API_URL + "key/api/v1/text2image/run"
STATUS_ENDPOINT = API_URL + "key/api/v1/text2image/status/"

headers = {
    'X-Key': f'Key {fusion_brain_token}',
    'X-Secret': f'Secret {fusion_brain_key}',
}


def get_text_to_image_kb() -> ReplyKeyboardMarkup:
    text_to_image_button = KeyboardButton(text="Text to image")
    buttons_row_1 = [text_to_image_button]
    markup_keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons_row_1],
        resize_keyboard=True
    )
    return markup_keyboard


# Class to interact with Text2Image API
class Text2ImageAPI:
    def __init__(self, url, fusion_brain_token, fusion_brain_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {fusion_brain_token}',
            'X-Secret': f'Secret {fusion_brain_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)


@router.message(Command("start_kadinsky", prefix="!/"))
async def start(message: types.Message):
    await message.answer(
        "Welcome to the Kandinsky bot! Please choose an option:",
        reply_markup=get_text_to_image_kb()
    )


@router.message(F.text == ButtonTextKadinsky.TEXT_TO_IMAGE)
async def handle_text_to_image(message: Message, state: FSMContext):
    await state.set_state(KadinskyStates.Intro)
    await message.answer("Please enter the text you want to generate an image for:")
    await state.set_state(KadinskyStates.TextToImage)


@router.message(KadinskyStates.TextToImage)
async def process_text_for_image(message: types.Message, state: FSMContext):
    await state.set_state(KadinskyStates.TextToImage)
    text = message.text
    api = Text2ImageAPI(
        "https://api-key.fusionbrain.ai/",
        f"{fusion_brain_token}",
        f"{fusion_brain_key}"
    )
    model_id = api.get_model()
    if model_id:
        print(f"Model ID: {model_id}")
        uuid = api.generate(text, model_id)
        print(f"Image UUID: {uuid}")
        images = api.check_generation(uuid)

        if images:
            print(f"Images: {images}")

            # Extract and decode base64 image data
            image_base64 = images[0]
            image_data = base64.b64decode(image_base64)

            # Use BufferedInputFile or URLInputFile depending on your needs
            # Here, I'll demonstrate using BufferedInputFile
            buffered_input_file = types.input_file.BufferedInputFile(file=image_data, filename="image.jpg")

            # Send the image data as a photo
            await message.answer_photo(buffered_input_file)

        else:
            await message.answer("Error generating image. Please try again later.")
    else:
        await message.answer("Error fetching model ID. Please try again later.")

    await state.clear()
