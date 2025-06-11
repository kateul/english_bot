from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

update_fields_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Имя"), KeyboardButton(text="Фамилия")],
        [KeyboardButton(text="День"), KeyboardButton(text="Время")],
        [KeyboardButton(text="🔙 В главное меню")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)
