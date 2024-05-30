from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from database.database import library_of_articles, products_in_sale


def create_lybrary_keyboard() -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
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
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for num, product in products_in_sale.items():
        text = product[0]
        callback = str(num)
        kb_builder.row(InlineKeyboardButton(
            text=f'{text[:100]}',
            callback_data=callback
        ))
    return kb_builder.as_markup()