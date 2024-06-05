from aiogram import Bot ,F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery,  Message
from environs import Env

from keyboards.inlines_kb import (
    create_form_product_keyboard,
    create_a_delivery_form_keyboard
)
from keyboards.main_kb import start_no_kb
from lexicon.lexicon import LEXICON
from filters.filters import IsLastFirstNamePatronymic, IsPhoneNumber

router = Router()

storage = MemoryStorage()

user_dict: dict[int, dict[str, str | int | bool]] = {}

env = Env()  # Создаем экземпляр класса Env
env.read_env()

bot = Bot(token=env('BOT_TOKEN'))


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
        '<b>Пожалуйста, введите ваши фамилию имя отчество'
        'без знаков препинания</b>\n\n'
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


@router.message(StateFilter(FSMFillForm.fill_name), IsLastFirstNamePatronymic())
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
        IsPhoneNumber()
    )
async def process_phone_number_sent(message: Message, state: FSMContext):
    # Заполнение поля формы "phonenumber".
    # Отправка клавиатуры с выбором продукции
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
        text='В этом поле нужно указать свои номер телефона, цифрами, '
        'начиная "+" или "8"\nЕсли вы хотите прервать заполнение анкеты - '
        'отправьте команду /cancel'
    )


@router.callback_query(StateFilter(FSMFillForm.fill_change_product))
async def process_wish_news_press(callback: CallbackQuery, state: FSMContext):
    # Заполнение поля формы "shipping_method"
    await state.update_data(change_product=callback.data)
    await callback.message.edit_text(
        text='Спасибо! Товар добавлен в форму!\n'
        'Выберите удобный вам способ доставки\n\n'
        'Если вы хотите прервать заполнение анкеты - '
        'отправьте команду /cancel',
        reply_markup=create_a_delivery_form_keyboard()
    )
    await callback.answer()
    await state.set_state(FSMFillForm.fill_shipping_method)



@router.callback_query(StateFilter(FSMFillForm.fill_shipping_method))
async def process_wish_news_press(callback: CallbackQuery,state: FSMContext):
    # Заполнение поля формы "shipping_method", завершение заполнения формы
    await state.update_data(shipping_method=callback.data)
    form_info = await state.get_data()
    try:
        await bot.send_message(
            chat_id=env.int('SEND_MESSAGE_ID'),
            text=f'<b>Пользователь{callback.from_user.id} заполнил форму!</b>\n'
            f'\n<b>ФИО:</b>\n{form_info['name']}'
            f'\n<b>Адрес</b>\n{form_info['adres']}'
            f'\n<b>Номер телефона</b>\n{form_info['phonenumber']}'
            f'\n<b>Продукция:</b>\n{form_info['change_product']}'
            f'\n<b>Спобос доставки:</b>\n{form_info['shipping_method']}',
            parse_mode='HTML'
        )
    except Exception:
        await callback.message.answer("Ошибка отправки.")
    await callback.answer()
    await state.clear()
    await callback.message.answer('Спасибо что заполнили форму')
