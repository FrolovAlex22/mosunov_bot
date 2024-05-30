from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message
# from database.database import user_dict_template, users_db
from filters.filters import IsDigitCallbackData
from keyboards.inlines_kb import create_lybrary_keyboard, create_product_keyboard
from keyboards.main_kb import start_no_kb
# from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON
from database.database import library_of_articles, products_in_sale
# from services.file_handling import book

router = Router()


storage = MemoryStorage()


user_dict: dict[int, dict[str, str | int | bool]] = {}


class FSMFillForm(StatesGroup):
    fill_name = State()
    fill_adres = State()
    fill_phonenumber = State()
    upload_photo = State()
    fill_change_product = State()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text], reply_markup=start_no_kb)


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


@router.message(Command(commands='formtosend'))
async def process_formtosend_command(message: Message):
    await message.answer(LEXICON[message.text])


@router.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    await message.answer(LEXICON[message.text])


@router.message(Command(commands='library'))
async def process_library_command(message: Message):
    if library_of_articles:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_lybrary_keyboard()
        )
    else:
        await message.answer(text=LEXICON['no_library'])


@router.message(F.text == LEXICON['library_button'])
async def process_yes_answer(message: Message):
    if library_of_articles:
        await message.answer(
            text=LEXICON['/library'],
            reply_markup=create_lybrary_keyboard()
        )
    else:
        await message.answer(text=LEXICON['no_library'])


@router.message(F.text == LEXICON['product'])
async def process_yes_answer(message: Message):
    if products_in_sale:
        await message.answer(
            text=LEXICON['product_button'],
            reply_markup=create_product_keyboard()
        )

@router.callback_query(IsDigitCallbackData())
async def process_backward_press(callback: CallbackQuery):
    name = products_in_sale[int(callback.data)][0]
    text = products_in_sale[int(callback.data)][1]
    price = products_in_sale[int(callback.data)][2]

    await callback.answer()
    await callback.message.answer(
        text=f'{name}\n\n{text}\nЦена: {price}руб.'
        )
    # await callback.message.answer_photo(
    #         photo=user_dict[message.from_user.id]['photo_id'],
