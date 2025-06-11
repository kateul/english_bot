from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_admin_keyboard():
    keyboard = [
        [KeyboardButton(text="👥 Список учеников")],
        [KeyboardButton(text="📢 Сделать рассылку")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
