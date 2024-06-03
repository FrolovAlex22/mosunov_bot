from aiogram import Router
from aiogram.types import Message

router = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@router.message()
async def send_echo(message: Message):
    await message.answer(
        'У этого бота не предусмотрена возможность переписываться '
        'если у вас возникли вопросы вы можете написать мне '
        'в телеграмм или ватсап по номеру 89997775566'
        )