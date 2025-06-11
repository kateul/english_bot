from aiogram.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import ADMIN_IDS

def get_main_menu(user_id: int) -> ReplyKeyboardMarkup:
    keyboard=[
        [KeyboardButton(text="📚 Мои занятия"),KeyboardButton(text="💰 Тарифы")],
        [KeyboardButton(text="📝 Регистрация"), KeyboardButton(text="✏️ Изменить данные")],
        [KeyboardButton(text="🔔 Включить напоминания"), KeyboardButton(text="🔕 Отключить напоминания")],
        [KeyboardButton(text="💬 Помощь"), KeyboardButton(text="✉️ Обратная связь")]
    ]

    if user_id in ADMIN_IDS:
        keyboard.append([KeyboardButton(text="Админ")])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
