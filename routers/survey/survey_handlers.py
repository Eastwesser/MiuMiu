from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command  # instead of CommandFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown  # чтобы была единая разметка при поступлении текста на вход

from keyboards.on_start import build_yes_or_no_keyboard
from validators.email_validators import valid_email_filter
from .states import Survey

router = Router(name="__name__")


@router.message(Command("survey", prefix="!/"))
async def handle_start_survey(
        message: types.Message,
        state: FSMContext
):
    await state.set_state(Survey.full_name)
    await message.answer(
        "Welcome to our weekly survey! What's your name?",
        reply_markup=types.ReplyKeyboardRemove()
    )


@router.message(Survey.full_name, F.text)
async def handle_survey_user_full_name(
        message: types.Message,
        state: FSMContext
):
    await state.update_data(full_name=message.text)
    await state.set_state(Survey.city)
    await message.answer(
        f"Hello, {markdown.hbold(message.text)}, now please enter your city",
        parse_mode=ParseMode.HTML
    )


@router.message(Survey.city, F.text)
async def handle_survey_city(
        message: types.Message,
        state: FSMContext
):
    await state.update_data(city=message.text)
    await state.set_state(Survey.email)
    await message.answer(
        "Now please share your email:"
    )


@router.message(Survey.email, valid_email_filter)
async def handle_survey_email_message(
        message: types.Message,
        state: FSMContext,
        email: str
):
    await state.update_data(email=email)
    await state.set_state(Survey.phone)
    await message.answer(
        "Please enter your phone number:"
    )


@router.message(Survey.phone, F.text)
async def handle_survey_phone(
        message: types.Message,
        state: FSMContext
):
    await state.update_data(phone=message.text)
    await state.set_state(Survey.email_newsletter)
    await message.answer(
        "Would you like to be informed in the future?",
        reply_markup=build_yes_or_no_keyboard()
    )


@router.message(Survey.email_newsletter, F.text.casefold() == "yes")
async def handle_survey_email_newsletter_ok(
        message: types.Message,
        state: FSMContext
):
    data = await state.update_data(newsletter_ok=True)
    await state.clear()
    await send_survey_results(message, data)


@router.message(Survey.email_newsletter, F.text.casefold() == "no")
async def handle_survey_email_newsletter_not_ok(
        message: types.Message,
        state: FSMContext
):
    data = await state.update_data(newsletter_ok=False)
    await state.clear()
    await send_survey_results(message, data)


async def send_survey_results(message: types.Message, data: dict) -> None:
    text = markdown.text(
        "Your survey results:",
        "",
        markdown.text("Name:", markdown.hbold(data["full_name"])),
        markdown.text("City:", markdown.hcode(data["city"])),
        markdown.text("Email:", markdown.hcode(data["email"])),
        markdown.text("Phone:", markdown.hcode(data["phone"])),
        ("Cool, we'll send you our news!" if data["newsletter_ok"] else "And we won't bother you again."),
        sep="\n",
    )
    await message.answer(
        text=text,
        reply_markup=types.ReplyKeyboardRemove()
    )


@router.message(Survey.email_newsletter)
async def handle_survey_email_newsletter_could_not_understand(message: types.Message):
    await message.answer(
        text="Sorry, I didn't understand, please send 'yes' or 'no'",
        reply_markup=build_yes_or_no_keyboard()
    )


@router.message(Survey.full_name)
async def handle_survey_user_full_name_invalid_content_type(message: types.Message):
    await message.answer(
        "Sorry, I don't understand. Send your full name as text."
    )


@router.message(Survey.email)
async def handle_survey_invalid_email_message(message: types.Message):
    await message.answer(
        "Invalid e-mail, try again, including '@' and '.' symbols!"
    )
