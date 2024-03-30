import os

import aiohttp
from aiogram import Bot, types, Dispatcher
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

from keyboards.inline_keyboards.actions_kb import build_actions_kb

bot_token = os.getenv('BOT_TOKEN')
load_dotenv()

bot = Bot(token=bot_token)
dp = Dispatcher()

router = Router(name=__name__)

# MEME BOX
MEME_COUNT = 10


@router.message(Command("memes", prefix="!/"))
async def give_meme(message: types.Message):
    folder_path = os.path.join(os.getcwd(), "routers", "custom", "photobot", "meme_box")
    file_count = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])

    if file_count == 0:
        await message.reply("No memes found :(")
        return

    for i in range(1, file_count + 1):
        file_name = str(i) + ".jpg"
        file_path = os.path.join(folder_path, file_name)

        photo = FSInputFile(file_path)
        await message.reply_photo(photo, caption="Here you are")

    await message.reply("That's all for now :3")


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
