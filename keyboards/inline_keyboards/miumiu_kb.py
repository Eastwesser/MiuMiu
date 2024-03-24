from enum import IntEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MiuMiuActions(IntEnum):
    meow = auto()
    hiss = auto()
    miu_root = auto()


class MiuMiuCbData(CallbackData, prefix="miumiu_actions"):
    action: MiuMiuActions


class CatMoodActions(IntEnum):
    details = auto()
    update = auto()
    price = auto()
    delete = auto()


class CatMoodCbData(CallbackData, prefix="mood"):
    action: CatMoodActions
    id: int
    title: str
    mood_score: int


def build_miumiu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="😻 Nya, daisuki!",
        callback_data=MiuMiuCbData(action=MiuMiuActions.meow).pack(),
    )
    builder.button(
        text="😾 Hssss!",
        callback_data=MiuMiuCbData(action=MiuMiuActions.hiss).pack(),
    )
    builder.adjust(1)  # каждая кнопка на новой строчке
    return builder.as_markup()


def build_meow_hiss_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Back to miu_root",
        callback_data=MiuMiuCbData(action=MiuMiuActions.miu_root).pack(),
    )
    for idx, (name, mood_score) in enumerate(
            [
                ("Meow", 10),
                ("Yawn", 5),
                ("Hiss", 0),
            ],
            start=1
    ):
        builder.button(
            text=name,
            callback_data=CatMoodCbData(
                action=CatMoodActions.details,
                id=idx,
                title=name,
                mood_score=mood_score,
            ),
        )
    builder.adjust(1)
    return builder.as_markup()


def cat_mood_details_kb(
        cat_mood_cb_data: CatMoodCbData
) -> InlineKeyboardMarkup:  # создаем клавиатуру, которая будет возвращать InlineKeyboardMarkup
    builder = InlineKeyboardBuilder()
    builder.button(
        text="😻 Nya, you're back! Daisuki!",
        callback_data=MiuMiuCbData(action=MiuMiuActions.meow).pack(),
    )
    for label, action in [
        ("Update", CatMoodActions.update),
        ("Delete", CatMoodActions.delete),
    ]:
        builder.button(
            text=label,  # кнопка update
            callback_data=CatMoodCbData(
                action=action,
                **cat_mood_cb_data.model_dump(include={"id", "title", "mood_score"}),
            )
        )
    builder.adjust(1, 2)
    return builder.as_markup()


def build_update_mood_kb(
    cat_mood_cb_data: CatMoodCbData,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=f"⬅ back to {cat_mood_cb_data.title}",
        callback_data=CatMoodCbData(
            action=CatMoodActions.details,
            **cat_mood_cb_data.model_dump(include={"id", "title", "mood_score"}),
        ),
    )
    builder.button(
        text="🔄 Update",
        callback_data=CatMoodCbData(
            action=CatMoodActions.update,
            **cat_mood_cb_data.model_dump(include={"id", "title", "mood_score"}),
        ).pack(),
    )
    return builder.as_markup()
