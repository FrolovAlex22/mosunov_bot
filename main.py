from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F

answers = [
    'У тебя все получиться не сомневайся',
    'Хорошие перспективы',
    'Еще немного и ты получишь желаемый результат',
    'Дорогу осилит идущий',
    'Все будет хорошо, я точно знаю'
    ]

BOT_TOKEN = '6799480724:AAHaPHLbMteAi2QPK4o9FiWz_wCKzMvKL74'

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nя генератор случайных предсказаний!\nНапиши мне что-нибудь')


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое предсказание'
    )


@dp.message(Command(commands=['sanek']))
async def process_help_command(message: Message):
    await message.answer(
        'А это я так...\nДля практики'
    )


@dp.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(
            text='Данный тип апдейтов не поддерживается '
                 'методом send_copy'
        )



if __name__ == '__main__':
    dp.run_polling(bot)
