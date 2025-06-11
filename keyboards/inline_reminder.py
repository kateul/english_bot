from aiogram.filters import callback_data
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

reminder_options = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⏰ За 1 час", callback_data="reminder_hour")],
    [InlineKeyboardButton(text="📅 За 1 день", callback_data="reminder_day")]
])