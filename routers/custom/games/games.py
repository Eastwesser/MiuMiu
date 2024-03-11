import random

from aiogram import Router
from aiogram import types
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message

router = Router(name=__name__)

CHOICES = ["Rock", "Paper", "Scissors"]


def build_rps_keyboard() -> InlineKeyboardMarkup:
    keyboard_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=choice, callback_data=f"rps_{choice.lower()}")
            ] for choice in CHOICES
        ]
    )
    return keyboard_markup


# Command handler to start Rock-Paper-Scissors game
@router.message(Command("rps", prefix="!/"))
async def start_rps_game(message: types.Message):
    # Get the keyboard for Rock-Paper-Scissors game
    keyboard_markup = build_rps_keyboard()

    # Send a message with the keyboard
    await message.answer("Choose your move:", reply_markup=keyboard_markup)


# Callback query handler to process Rock-Paper-Scissors move
@router.callback_query(lambda callback_query: callback_query.data.startswith("rps_"))
async def process_rps_move(callback_query: types.CallbackQuery):
    user_choice = callback_query.data.split("_")[1].capitalize()
    bot_choice = random.choice(CHOICES)

    # Determine the winner
    winner = determine_winner(user_choice, bot_choice)

    # Send the result
    await callback_query.answer(f"Bot chose {bot_choice}. {winner}")


# Function to determine the winner of Rock-Paper-Scissors game
def determine_winner(user_choice, bot_choice):
    if user_choice == bot_choice:
        return "It's a tie!"
    elif (user_choice == "Rock" and bot_choice == "Scissors") or \
            (user_choice == "Paper" and bot_choice == "Rock") or \
            (user_choice == "Scissors" and bot_choice == "Paper"):
        return "You win!"
    else:
        return "Bot wins!"


# DICE EMOJI BOT
@router.message(Command("bowling", prefix="!/"))
async def play_games(message: Message):
    x = await message.answer_dice(DiceEmoji.BOWLING)
    print(x.dice.value)


@router.message(Command("dice", prefix="!/"))
async def play_games1(message: Message):
    x = await message.answer_dice(DiceEmoji.DICE)
    print(x.dice.value)


@router.message(Command("casino", prefix="!/"))
async def play_games1(message: Message):
    x = await message.answer_dice(DiceEmoji.SLOT_MACHINE)
    print(x.dice.value)


@router.message(Command("dart", prefix="!/"))
async def play_games2(message: Message):
    x = await message.answer_dice(DiceEmoji.DART)
    print(x.dice.value)


@router.message(Command("basketball", prefix="!/"))
async def play_games2(message: Message):
    x = await message.answer_dice(DiceEmoji.BASKETBALL)
    print(x.dice.value)


@router.message(Command("football", prefix="!/"))
async def play_games2(message: Message):
    x = await message.answer_dice(DiceEmoji.FOOTBALL)
    print(x.dice.value)


@router.message(Command("hearts", prefix="!/"))  # Обработчик команды для игры в Черви
async def play_hearts(message: Message):
    hearts_faces = ["❤️", "♠️", "♦️", "♣️"]  # Список символов мастей
    hearts_values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]  # Список значений карт
    card = random.choice(hearts_values) + random.choice(hearts_faces)  # Выбор случайной карты
    await message.answer(f"Your card is: {card}")  # Отправка сообщения с картой игроку
