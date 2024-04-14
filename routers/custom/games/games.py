import asyncio
import copy
import logging
import random
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram import Router, types
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

router = Router(name=__name__)

CHOICES = ["Rock", "Paper", "Scissors"]

WINS_REQUIRED = 3
BLACKJACK_FACES = ["❤️", "♠️", "♦️", "♣️"]
BLACKJACK_VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

round_number = 1
health_p1 = 10
health_p2 = 10

logging.basicConfig(level=logging.DEBUG)


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


# DICE EMOJI BOT =======================================================================================================
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


# BLACKJACK ============================================================================================================
class BlackjackMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
            message: types.Message,
            data: Dict[str, Any]
    ) -> Any:
        # Implement your middleware logic here
        result = await handler(message, data)
        return result


def deal_card():
    return random.choice(BLACKJACK_FACES), random.choice(BLACKJACK_VALUES)


# Global variables for player and dealer hands
player_hand = []
dealer_hand = []


# Handler for the /startblackjack command
@router.message(Command("start_blackjack", prefix="!/"))
async def start_blackjack(message: types.Message):
    await message.answer("Hi! Welcome to Blackjack. Send /play21 to start playing.")


# Handler for the /play21 command
@router.message(Command("play21", prefix="!/"))
async def play_blackjack(message: types.Message):
    global player_hand, dealer_hand
    player_hand = [deal_card(), deal_card()]
    dealer_hand = [deal_card(), deal_card()]

    player_score = calculate_hand_score(player_hand)
    dealer_score = calculate_hand_score(dealer_hand)

    player_message = f"Your hand: {player_hand}\nYour score: {player_score}"
    dealer_message = f"Dealer's hand: [{dealer_hand[0]}, ???]\nDealer's score: {dealer_hand[0][1]}"

    await message.answer(player_message)
    await message.answer(dealer_message)
    await message.answer("Type /hit to get a card or /stand to end your turn.")


# Handler for the /hit command
@router.message(Command("hit", prefix="!/"))
async def hit_blackjack(message: types.Message):
    global player_hand
    card = deal_card()
    player_hand.append(card)

    player_score = calculate_hand_score(player_hand)
    await message.answer(f"You drew: {card}. Your score: {player_score}")

    if player_score > 21:
        await message.answer("You bust! Dealer wins.")
        reset_game()


# Handler for the /stand command
@router.message(Command("stand", prefix="!/"))
async def stand_blackjack(message: types.Message):
    global dealer_hand
    while calculate_hand_score(dealer_hand) < 17:
        dealer_hand.append(deal_card())

    dealer_score = calculate_hand_score(dealer_hand)
    await message.answer(f"Dealer's hand: {dealer_hand}. Dealer's score: {dealer_score}")

    player_score = calculate_hand_score(player_hand)
    if player_score > 21 or player_score < dealer_score <= 21:
        await message.answer("Dealer wins!")
    elif dealer_score > 21 or player_score > dealer_score:
        await message.answer("You win!")
    elif player_score == dealer_score:
        await message.answer("It's a tie!")

    reset_game()


# Function to calculate the score of a hand in blackjack
def calculate_hand_score(hand):
    score = 0
    ace_count = 0
    for card in hand:
        value = card[1]
        if value.isdigit():
            score += int(value)
        elif value in ('J', 'Q', 'K'):
            score += 10
        elif value == 'A':
            ace_count += 1
            score += 11
    while ace_count > 0 and score > 21:
        score -= 10
        ace_count -= 1
    return score


# Function to reset the game
def reset_game():
    global player_hand, dealer_hand
    player_hand = []
    dealer_hand = []


# BLOCK ME =============================================================================================================
@router.message(Command("start_block_me", prefix="!/"))
async def start_blockme_game(message: types.Message):
    global round_number, health_p1, health_p2
    round_number = 1
    health_p1 = 10
    health_p2 = 10

    block_me_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="^", callback_data="hit_head"),
                InlineKeyboardButton(text=">", callback_data="hit_chest"),
                InlineKeyboardButton(text="v", callback_data="hit_legs")
            ]
        ]
    )

    # Send the message with the keyboard
    await message.answer("Round 1. Player 2, choose an attack:", reply_markup=block_me_kb)


@router.callback_query(lambda callback_query: callback_query.data.startswith("hit_"))
async def process_blockme_attack(callback_query: types.CallbackQuery):
    global health_p1, health_p2, round_number
    choice_p2 = callback_query.data
    choice_p1 = random.choice(["hit_head", "hit_chest", "hit_legs"])  # Random choice for player 1's defense

    if choice_p2 == choice_p1:
        round_result = "Player 1 defended successfully"
    elif (choice_p2 == "hit_head" and choice_p1 == "hit_legs") or \
            (choice_p2 == "hit_chest" and choice_p1 == "hit_legs") or \
            (choice_p2 == "hit_legs" and choice_p1 == "hit_head"):
        round_result = "Player 1 lost 2 health points"
        health_p1 -= 2
    else:
        round_result = "Player 1 lost 1 health point"
        health_p1 -= 1

    await callback_query.answer(f"{round_result}\n"
                                f"Player 1 health: {health_p1}\n"
                                f"Player 2 health: {health_p2}")

    # Check if any player's health is 0 or below
    if health_p1 <= 0:
        await callback_query.message.reply("Player 1 is defeated! GAME OVER")
    elif health_p2 <= 0:
        await callback_query.message.reply("Player 2 is defeated! GAME OVER")
    else:
        # Build the keyboard and send the message for the next round
        await asyncio.sleep(5)


# SEA BATTLE ===========================================================================================================
# Инициализируем константу размера игрового поля
FIELD_SIZE = 8

# Создаем словарь соответствий
LEXICON = {
    '/start': 'Вот твое поле. Можешь делать ход',
    '/start_naval': 'Your message for /start_naval command goes here',
    0: ' ',
    1: '🌊',
    2: '💥',
    'miss': 'Мимо!',
    'hit': 'Попал!',
    'used': 'Вы уже стреляли сюда!',
    'next_move': 'Делайте ваш следующий ход'
}

# Хардкодим расположение кораблей на игровом поле
ships: list[list[int]] = [
    [1, 0, 1, 1, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0]
]

# Инициализируем "базу данных" пользователей
users: dict[int, dict[str, list]] = {}


# Создаем свой класс фабрики коллбэков, указывая префикс
# и структуру callback_data
class FieldCallbackFactory(CallbackData, prefix="user_field"):
    x: int
    y: int


# Функция, которая пересоздает новое поле для каждого игрока
def reset_field(user_id: int) -> None:
    users[user_id]['ships'] = copy.deepcopy(ships)
    users[user_id]['field'] = [
        [0 for _ in range(FIELD_SIZE)]
        for _ in range(FIELD_SIZE)
    ]


# Функция, генерирующая клавиатуру в зависимости от данных из
# матрицы ходов пользователя
def get_field_keyboard(user_id: int) -> InlineKeyboardMarkup:
    array_buttons: list[list[InlineKeyboardButton]] = []

    for i in range(FIELD_SIZE):
        array_buttons.append([])
        for j in range(FIELD_SIZE):
            array_buttons[i].append(InlineKeyboardButton(
                text=LEXICON[users[user_id]['field'][i][j]],
                callback_data=FieldCallbackFactory(x=i, y=j).pack()
            ))

    return InlineKeyboardMarkup(inline_keyboard=array_buttons)


# Этот хэндлер будет срабатывать на команду /start, записывать
# пользователя в "базу данных", обнулять игровое поле и отправлять
# пользователю сообщение с клавиатурой
@router.message(Command("start_naval", prefix="!/"))
async def process_start_command(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {}
    reset_field(message.from_user.id)
    await message.answer(
        text=LEXICON['/start_naval'],
        reply_markup=get_field_keyboard(message.from_user.id)
    )


# Этот хэндлер будет срабатывать на нажатие любой инлайн-кнопки на поле,
# запускать логику проверки результата нажатия и формирования ответа
@router.callback_query(FieldCallbackFactory.filter())
async def process_category_press(callback: CallbackQuery,
                                 callback_data: FieldCallbackFactory):
    field = users[callback.from_user.id]['field']
    ships = users[callback.from_user.id]['ships']
    if field[callback_data.x][callback_data.y] == 0 and \
            ships[callback_data.x][callback_data.y] == 0:
        answer = LEXICON['miss']
        field[callback_data.x][callback_data.y] = 1
    elif field[callback_data.x][callback_data.y] == 0 and \
            ships[callback_data.x][callback_data.y] == 1:
        answer = LEXICON['hit']
        field[callback_data.x][callback_data.y] = 2
    else:
        answer = LEXICON['used']

    try:
        await callback.message.edit_text(
            text=LEXICON['next_move'],
            reply_markup=get_field_keyboard(callback.from_user.id)
        )
    except TelegramBadRequest:
        pass

    await callback.answer(answer)


# Five cats memory game ================================================================================================
sticker_ids = [
    "CAACAgIAAxkBAU4nKGYa5ZK0jTMFY5e2XYYrkGZDqCS1AAJVPQACxW34SnUXpLRodIq0NAQ",  # first_cat_sticker_id
    "CAACAgIAAxkBAU4nRmYa5lH4SBbRLWwBjKwR_84afmr-AAIsNgACNZvxSvKNYjzvkYigNAQ",  # second_cat_sticker_id
    "CAACAgIAAxkBAU4nQ2Ya5kI8KwXCzSAce4WvCnhOzi_8AAJUPAACRboJS3juH0a3Q8ocNAQ",  # third_cat_sticker_id
    "CAACAgIAAxkBAU4nPmYa5ey_nB6hS9dX71eZL7WmJ63iAAKXPQACuSLwSqDsP1hlPM6sNAQ",  # fourth_cat_sticker_id
    "CAACAgIAAxkBAU4nSmYa5mRSn-CFZFkO_hyI_gdKqiN-AALjOAACwVwIS78AAfOpYkBUmjQE"  # fifth_cat_sticker_id
]

correct_sequence = list(range(1, 6))

# Dictionary to store user's choices
user_choices = {}


@router.message(Command("start_five_cats", prefix="!/"))
async def start_five_cats(message: types.Message):
    await message.answer("Hi! Welcome to Five Cats. Send /play_five_cats to start playing.")


async def show_random_cats(chat_id, bot):
    # Shuffle the order of cat sticker IDs
    random.shuffle(sticker_ids)

    # Display the shuffled cats
    for i, cat_id in enumerate(sticker_ids, start=1):
        await asyncio.sleep(2)  # Wait for 2 seconds
        await bot.send_sticker(chat_id, cat_id)
        await bot.send_message(chat_id, f"Cat {i}")


@router.message(Command("play_five_cats", prefix="!/"))
async def play_five_cats(message: types.Message):
    await message.answer("Get ready! The cats will appear shortly...")
    await asyncio.sleep(2)  # Wait for 2 seconds

    # Pass the bot object to the show_random_cats function
    await show_random_cats(message.chat.id, message.bot)

    # Clear user choices
    user_id = message.from_user.id
    user_choices[user_id] = []

    # Show the keyboard for user selection
    five_cats_buttons = [
        [InlineKeyboardButton(text='Рыжик', callback_data='1')],
        [InlineKeyboardButton(text='Сиамочка', callback_data='2')],
        [InlineKeyboardButton(text='Снежок', callback_data='3')],
        [InlineKeyboardButton(text='Тортик', callback_data='4')],
        [InlineKeyboardButton(text='Фиалка', callback_data='5')],
    ]
    inline_kb = InlineKeyboardMarkup(inline_keyboard=five_cats_buttons)

    await message.answer("Now choose the correct order!", reply_markup=inline_kb)


async def compare_choices(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_choices_list = user_choices[user_id]

    # Check if user_choices_list matches the correct_sequence
    if user_choices_list == correct_sequence:
        await callback_query.message.answer("Good job, your memory is fine :3 Play again? /play_five_cats")
    else:
        # Find the index of the first mismatch
        index = next((i for i, (x, y) in enumerate(zip(user_choices_list, correct_sequence)) if x != y), None)
        await callback_query.message.answer(f"You have mistakes! The correct sequence is: {correct_sequence}")


@router.callback_query(lambda c: c.data.isdigit() and int(c.data) in range(1, 6))
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    choice_number = int(callback_query.data)
    user_choices[user_id].append(choice_number)

    # Get the index of the current cat
    current_cat_index = len(user_choices[user_id])

    # Check if the current cat chosen by the user matches the correct sequence
    if choice_number == correct_sequence[current_cat_index - 1]:
        await callback_query.message.answer("Угадали!")
    else:
        await callback_query.message.answer("Wrong choice! Try again.")

    # If the user has made all 5 choices, provide the correct sequence
    if current_cat_index == 5:
        await compare_choices(callback_query)
    else:
        # Prompt the user to select the next cat
        await callback_query.message.answer(f"Now choose Cat {current_cat_index + 1}")
