# common keyboards
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButtonPollType,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class ButtonText:
    HELLO = "Hello!"
    WHATS_NEXT = "What's next?"
    BYE = "Good bye!"


def get_on_start_kb() -> ReplyKeyboardMarkup:  # аннотация, что возвращаем ReplyKeyboardMarkup
    button_hello = KeyboardButton(text=ButtonText.HELLO)
    button_help = KeyboardButton(text=ButtonText.WHATS_NEXT)
    button_bye = KeyboardButton(text=ButtonText.BYE)
    buttons_row_1 = [button_hello, button_help]  # список из кнопок 1 (первая строка)
    buttons_row_2 = [button_bye]  # список из кнопок 2 (вторая строка)
    markup_keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons_row_1,
                  buttons_row_2],
        resize_keyboard=True,  # позволяет подбить кнопку под размер строки
    )  # разметка клавиатуры
    return markup_keyboard


def get_on_help_kb():
    numbers = [
        "/weather",
        "/converter",
        "/calculator",
        "/food",
        "/sticker_kb",
        "/magnetic_storm",
        "/memes",
        "/start_blockme",
        "/rps",
        "/startblackjack",
    ]
    buttons_row = [KeyboardButton(text=num) for num in numbers]
    #
    # markup = ReplyKeyboardMarkup(
    #     keyboard=[buttons_row],
    #     resize_keyboard=True,  # позволяет подбить кнопку под размер строки, а лимит строки 12 символов
    # )
    # return markup
    builder = ReplyKeyboardBuilder()
    for num in numbers:
        builder.add(KeyboardButton(text=num))
    # builder.button(text=num) то же самое, что и сверху
    # builder.adjust(3, 3, 4)  # все строчки будут перестроены, чтобы было по 3 символа в строке (3);
    builder.adjust(3)
    builder.row(buttons_row[3], buttons_row[1])  # сюда добавляем кнопки, располагаются в одну новую строчку
    # builder.add(buttons_row[-1])
    # и 3 значения на первой строке, 3 на второй, 4 на последней, если указывать явно (3,3,4)
    return builder.as_markup(resize_keyboard=False)  # возвращаем builder как markup, чтобы у нас была разметка


def get_actions_kb() -> ReplyKeyboardMarkup:
    # markup = ReplyKeyboardMarkup(
    #     input_field_placeholder=
    #     keyboard=[]
    # )
    # return markup
    builder = ReplyKeyboardBuilder()
    # builder.add(KeyboardButton(text="Send Location 🌍", request_location=True))
    builder.button(
        text="🌍 Send Location",
        request_location=True,
    )
    builder.button(
        text="📱 Send My Phone",
        request_contact=True,
    )
    builder.button(
        text="📊 Send Poll",
        request_poll=KeyboardButtonPollType(),
    )
    builder.button(
        text="❓ Send Quiz",
        request_poll=KeyboardButtonPollType(type="quiz"),
    )
    builder.button(
        text="❔ Regular Quiz",
        request_poll=KeyboardButtonPollType(type="regular"),
    )
    builder.button(
        text=ButtonText.BYE,
    )
    builder.adjust(1)  # все на одну строчку, по одному элементу
    return builder.as_markup(
        input_field_placeholder="Actions:",
        resize_keyboard=True,
    )
    # NOTE: resize_keyboard=True позволяет нормализовать размер кнопки
