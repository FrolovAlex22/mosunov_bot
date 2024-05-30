from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON

button_library = KeyboardButton(text=LEXICON['library_button'])
button_product = KeyboardButton(text=LEXICON['product'])
button_form = KeyboardButton(text=LEXICON['form_button'])


start_kb_builder = ReplyKeyboardBuilder()

start_kb_builder.row(button_library, button_product, button_form, width=1)

start_no_kb: ReplyKeyboardMarkup = start_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
    )
