from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from database.database import library_of_articles, products_in_sale


def create_lybrary_keyboard() -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры с библиотекой полезной информации
    kb_builder = InlineKeyboardBuilder()
    for _, meaning in library_of_articles.items():
        text = meaning[0]
        url = meaning[1]
        kb_builder.row(InlineKeyboardButton(
            text=f'{text[:100]}',
            url=url
        ))
    return kb_builder.as_markup()


def create_product_keyboard() -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    for num, product in products_in_sale.items():
        text = product[0]
        callback = str(num)
        kb_builder.row(InlineKeyboardButton(
            text=f'{text[:100]}',
            callback_data=callback
        ))
    return kb_builder.as_markup()


def create_form_product_keyboard() -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    first_button = InlineKeyboardButton(
        text='Отвсехболезнит',
        callback_data='Отвсехболезнит'
    )
    secotd_button = InlineKeyboardButton(
        text='Еслибольнопомогит',
        callback_data='Еслибольнопомогит'
    )
    third_button = InlineKeyboardButton(
        text='Здоровъесохранит',
        callback_data='Здоровъесохранит'
    )
    keyboard: list[list[InlineKeyboardButton]] = [
        [first_button],[secotd_button],[third_button]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    return markup