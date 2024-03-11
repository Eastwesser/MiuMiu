from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from keyboards.inline_keyboards.miumiu_kb import (
    MiuMiuActions,
    MiuMiuCbData,
    build_miumiu_kb,
    build_meow_hiss_kb,
    CatMoodActions,
    CatMoodCbData, cat_mood_details_kb, build_update_mood_kb,
)

router = Router(name=__name__)


@router.callback_query(
    MiuMiuCbData.filter(F.action == MiuMiuActions.miu_root)
)
async def handle_meow_button(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        text="Your cat's meow actions: ",
        reply_markup=build_miumiu_kb(),
        cache_time=10,
    )


@router.callback_query(
    MiuMiuCbData.filter(F.action == MiuMiuActions.meow)
)
async def handle_meow_button(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        text="Available cat's mood sounds",
        reply_markup=build_meow_hiss_kb(),
    )


@router.callback_query(
    MiuMiuCbData.filter(F.action == MiuMiuActions.hiss),
)
async def handle_my_address_button(call: CallbackQuery):
    await call.answer(
        "The hiss section is still in progress...",
        cache_time=30,
    )


@router.callback_query(
    CatMoodCbData.filter(F.action == CatMoodActions.details)
)
async def handle_cat_mood_details_button(
        call: CallbackQuery,
        callback_data: CatMoodCbData,
):
    await call.answer()
    message_text = markdown.text(
        markdown.hbold(f"Sound №{callback_data.id}"),
        markdown.text(
            markdown.hbold("Title: "),
            callback_data.title,
        ),
        markdown.text(
            markdown.hbold("Mood score: "),
            callback_data.mood_score,
        ),
        sep="\n",
    )
    await call.message.edit_text(
        text=message_text,  # добавляем информацию о звуках
        reply_markup=cat_mood_details_kb(callback_data),
    )


@router.callback_query(
    CatMoodCbData.filter(F.action == CatMoodActions.delete)
)
async def handle_product_delete_button(
        call: CallbackQuery,
):
    await call.answer(
        text="Delete is still in progress...",
    )


@router.callback_query(
    CatMoodCbData.filter(F.action == CatMoodActions.update)
)
async def handle_product_update_button(
        call: CallbackQuery,
        callback_data: CatMoodCbData,
):
    await call.answer()
    await call.message.edit_reply_markup(
        reply_markup=build_update_mood_kb(callback_data),
    )
