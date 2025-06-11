from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

days_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Понедельник"), KeyboardButton(text="Вторник")],
        [KeyboardButton(text="Среда"), KeyboardButton(text="Четверг")],
        [KeyboardButton(text="Пятница"), KeyboardButton(text="Суббота")],
        [KeyboardButton(text="Воскресенье"),KeyboardButton(text="Вся неделя")],
        [KeyboardButton(text="↩ Назад в админ-панель")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True #Requests clients to hide the keyboard as soon as it's been used.
)