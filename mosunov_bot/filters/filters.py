from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message


class IsDigitCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.isdigit()


class IsLastFirstNamePatronymic(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text.replace(' ', '').isalpha()


class IsPhoneNumber(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return (
            message.text.isdigit() or
            (message.text[1:].isdigit() and message.text[0] == '+') and
            (len(message.text) == 11 or len(message.text) == 12)
        )
