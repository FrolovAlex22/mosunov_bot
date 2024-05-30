from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize)
# from database.database import user_dict_template, users_db
from filters.filters import IsDigitCallbackData
from keyboards.inlines_kb import create_lybrary_keyboard, create_product_keyboard
from keyboards.main_kb import start_no_kb
# from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON

router = Router()


storage = MemoryStorage()


user_dict: dict[int, dict[str, str | int | bool]] = {}


class FSMFillForm(StatesGroup):
    fill_name = State()
    fill_adres = State()
    fill_phonenumber = State()
    fill_change_product = State()


@router.message(F.text == LEXICON['form_button'])
async def process_formtosend_command(message: Message, state: FSMContext):
    await message.answer(
        text='Пожалуйста, введите ваши фамилию имя отчество'
        'без знаков препинания'
        )
    await state.set_state(FSMFillForm.fill_name)


@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего. Вы вне машины состояний\n\n'
             'Чтобы перейти к заполнению анкеты - '
             'отправьте команду /fillform'
    )


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вышли из машины состояний\n\n'
             'Чтобы снова перейти к заполнению анкеты - '
             'отправьте команду /fillform'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода возраста
@router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(name=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите ваш адрес')
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_adres)


# Этот хэндлер будет срабатывать, если во время ввода имени
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_name))
async def warning_not_name(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на имя\n\n'
             'Пожалуйста, введите ваше фамилию имя отвечтво, \n\n'
             'без знаков припинания'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )


@router.message(StateFilter(FSMFillForm.fill_adres), F.text)
async def process_age_sent(message: Message, state: FSMContext):
    await state.update_data(adres=message.text)
    await message.answer(text='Спасибо!\n\nВведите ваш номер телефона')
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_phonenumber)


@router.message(StateFilter(FSMFillForm.fill_adres))
async def warning_not_name(message: Message):
    await message.answer(
        text='В этом поле нужно указать свои адрес строкой'
             'отправьте команду /cancel'
    )


@router.message(
        StateFilter(FSMFillForm.fill_phonenumber),
        lambda x: x.text[1:].isdigit() or x.text.isdigit()
    )
async def process_age_sent(message: Message, state: FSMContext):
    await state.update_data(phonenumber=message.text)
    await message.answer(
        text='Спасибо!\n\nВыберите продукцию которая вас заинтересовала'
    )
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
    # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
    keyboard: list[list[InlineKeyboardButton]] = [
        [first_button, secotd_button],
        [third_button]
    ]
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Устанавливаем состояние ожидания ввода возраста
    await message.answer(
        text='Спасибо!\n\nВыберите продукцию которая вас интересует',
        reply_markup=markup
    )
    await state.set_state(FSMFillForm.fill_change_product)


@router.message(StateFilter(FSMFillForm.fill_phonenumber))
async def warning_not_name(message: Message):
    await message.answer(
        text='В этом поле нужно указать свои номер телефона, цифрами, начинаю я "+"'
             'отправьте команду /cancel'
    )


@router.callback_query(StateFilter(FSMFillForm.fill_change_product))
async def process_wish_news_press(callback: CallbackQuery, state: FSMContext):
    await state.update_data(change_product=callback.data)
    var = await state.get_data()
    await state.clear()
    await callback.message.edit_text(
        text='Спасибо! Ваши данные сохранены!\n\n'
             'Вы вышли из машины состояний'
    )
    await callback.message.answer(f'результат заполнения формы{var}')
