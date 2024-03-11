from enum import IntEnum, auto  # auto ставим, когда знаем, что значения не будут меняться

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class ShopActions(IntEnum):
    products = auto()  # на основе этого метода будет то же самое значение
    address = auto()
    root = auto()


class ShopCbData(CallbackData, prefix="shop"):
    action: ShopActions


class ProductActions(IntEnum):
    details = auto()
    update = auto()
    delete = auto()


class ProductCbData(CallbackData, prefix="product"):
    action: ProductActions
    id: int
    title: str
    price: int


def build_shop_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()  # здесь делаем кнопки
    builder.button(
        text="Show products",
        callback_data=ShopCbData(action=ShopActions.products).pack(),
    )
    builder.button(
        text="My address",
        callback_data=ShopCbData(action=ShopActions.address).pack(),
    )
    builder.adjust(1)  # каждая кнопка на новой строчке
    return builder.as_markup()


def build_products_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Back to root",
        callback_data=ShopCbData(action=ShopActions.root).pack(),
    )
    for idx, (name, price) in enumerate(
            [
                ("Tablet", 1000),
                ("Laptop", 1300),
                ("Desktop", 2500),
            ],
            start=1,
    ):
        builder.button(
            text=name,
            callback_data=ProductCbData(
                action=ProductActions.details,
                id=idx,
                title=name,
                price=price,
            ),
        )
    builder.adjust(1)
    return builder.as_markup()


def product_details_kb(
        product_cb_data: ProductCbData
) -> InlineKeyboardMarkup:  # создаем клавиатуру, которая будет возвращать InlineKeyboardMarkup
    builder = InlineKeyboardBuilder()
    builder.button(
        text="⬅ Back to products",  # кнопка возврата назад к списку товаров
        callback_data=ShopCbData(action=ShopActions.products).pack(),
    )
    for label, action in [
        ("Update", ProductActions.update),
        ("Delete", ProductActions.delete),
    ]:
        builder.button(
            # text="Update",  # кнопка update
            text=label,
            callback_data=ProductCbData(
                action=action,
                **product_cb_data.model_dump(include={"id", "title", "price"}),  # лучший выбор
                # OR **product_cb_data.model_dump(exclude={"actions"}), так мы передаем исключения
                # id=product_cb_data.id,
                # title=product_cb_data.title,
                # price=product_cb_data.price,
            ),
        )
    builder.adjust(1, 2)
    return builder.as_markup()


def build_update_product_kb(
    product_cb_data: ProductCbData,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=f"⬅ back to {product_cb_data.title}",
        callback_data=ProductCbData(
            action=ProductActions.details,
            **product_cb_data.model_dump(include={"id", "title", "price"}),
        ),
    )
    builder.button(
        text="🔄 Update",
        callback_data=...,
    )
    return builder.as_markup()
