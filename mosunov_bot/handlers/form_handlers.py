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
from keyboards.inlines_kb import create_form_product_keyboard
from keyboards.main_kb import start_no_kb
# from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON, LEXICON_COMMANDS

router = Router()


storage = MemoryStorage()


user_dict: dict[int, dict[str, str | int | bool]] = {}


class FSMFillForm(StatesGroup):
    fill_name = State()
    fill_adres = State()
    fill_phonenumber = State()
    fill_change_product = State()
    fill_shipping_method = State()


@router.message(Command(commands='formtosend'))
@router.message(F.text == LEXICON['formtosend'])
async def process_formtosend_command(message: Message, state: FSMContext):
    # Начало заполнения формы клиента
    await message.answer(
        text='Нужно заполнить несколько полей чтобы в дальнейшем '
        'я смог сориентироваться по цене и способе доставки\n\n'
        'Пожалуйста, введите ваши фамилию имя отчество'
        'без знаков препинания\n\n'
        'Если вы хотите прервать заполнение анкеты - '
        'отправьте команду /cancel'
        )
    await state.set_state(FSMFillForm.fill_name)


@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    # Попытка отмены заполнения формы в случае если форма не заполняеться
    await message.answer(
        text='Отменять нечего. Вы пока еще не приступили к заполнению формы\n\n'
        f'Чтобы перейти к заполнению анкеты - отправьте команду /formtosend'
    )


@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    # Отмена заполнения формы
    await message.answer(
        text='Вы прекратили заполнение формы\n\n',
        reply_markup=start_no_kb
    )
    await state.clear()


@router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    # Заполнение поля формы "name"
    await state.update_data(name=message.text)
    await message.answer(
        text='А теперь введите ваш адрес\n\n'
        'Если вы хотите прервать заполнение анкеты - '
        'отправьте команду /cancel'
    )
    await state.set_state(FSMFillForm.fill_adres)


@router.message(StateFilter(FSMFillForm.fill_name))
async def warning_not_name(message: Message):
    # Ввод неверных данных при заполнении поля формы "name"
    await message.answer(
        text='То, что вы отправили не похоже фамилию имя отвечтво\n\n'
             'Пожалуйста, введите ваше фамилию имя отвечтво,'
             'без знаков припинания\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )


@router.message(StateFilter(FSMFillForm.fill_adres), F.text)
async def process_adres_sent(message: Message, state: FSMContext):
    # Заполнение поля формы "adres"
    await state.update_data(adres=message.text)
    await message.answer(
        text='Введите ваш номер телефона\n\n'
        'Если вы хотите прервать заполнение анкеты - '
        'отправьте команду /cancel'
        )
    await state.set_state(FSMFillForm.fill_phonenumber)


@router.message(StateFilter(FSMFillForm.fill_adres))
async def warning_not_adres(message: Message):
    # Ввод неверных данных при заполнении поля формы "adres"
    await message.answer(
        text='В этом поле нужно указать свои адрес строкой\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )


@router.message(
        StateFilter(FSMFillForm.fill_phonenumber),
        lambda x: x.text[1:].isdigit() or x.text.isdigit()
    )
async def process_phone_number_sent(message: Message, state: FSMContext):
    # Заполнение поля формы "phonenumber"
    await state.update_data(phonenumber=message.text)
    await message.answer(
        text='Выберите продукцию которая вас интересует\n\n'
        'Если вы хотите прервать заполнение анкеты - '
        'отправьте команду /cancel',
        reply_markup=create_form_product_keyboard()
    )
    await state.set_state(FSMFillForm.fill_change_product)


@router.message(StateFilter(FSMFillForm.fill_phonenumber))
async def warning_not_phone_number(message: Message):
    # Ввод неверных данных при заполнении поля формы "phonenumber"
    await message.answer(
        text='В этом поле нужно указать свои номер телефона, цифрами,'
        'начиная "+"\nЕсли вы хотите прервать заполнение анкеты - '
        'отправьте команду /cancel'
    )


@router.callback_query(StateFilter(FSMFillForm.fill_change_product))
async def process_wish_news_press(callback: CallbackQuery, state: FSMContext):
    # Заполнение поля формы "phonenumber"
    post_button = InlineKeyboardButton(
        text='Почта России',
        callback_data='почтароссии'
    )
    cdek_button = InlineKeyboardButton(
        text='CDEK',
        callback_data='cdek'
    )
    await state.update_data(change_product=callback.data)
    keyboard: list[list[InlineKeyboardButton]] = [
        [post_button, cdek_button]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await callback.message.edit_text(
        text='Спасибо! Товар добавлен в форму!\n'
        'Выберите удобный вам способ доставки\n\n'
        'Если вы хотите прервать заполнение анкеты - '
        'отправьте команду /cancel',
        reply_markup=markup
    )
    await callback.answer()
    await state.set_state(FSMFillForm.fill_shipping_method)



@router.callback_query(StateFilter(FSMFillForm.fill_shipping_method))
async def process_wish_news_press(callback: CallbackQuery, state: FSMContext):
    # Заполнение поля формы "shipping_method", завершение заполнения формы
    await state.update_data(shipping_method=callback.data)
    form_info = await state.get_data()
    await state.clear()
    await callback.message.answer(f'Спасибо что заполнили форму\n\n{form_info}')
