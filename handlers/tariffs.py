from aiogram import Router, F, types
from db import get_tariffs_by_category
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.menu import get_main_menu  # Импорт главного меню


router = Router()

# Клавиатура с категориями
tariff_categories_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧒 Уроки для детей")],
        [KeyboardButton(text="👩‍💼 Уроки для взрослых")],
        [KeyboardButton(text="🎓 Подготовка к экзаменам")],
        [KeyboardButton(text="↩ Вернуться в меню")]
    ],
    resize_keyboard=True
)

@router.message(F.text == "💰 Тарифы")
async def show_tarifs_categories(message: types.Message):
    await message.answer("Выбери категорию тарифов:", reply_markup=tariff_categories_keyboard)

@router.message(F.text == "🧒 Уроки для детей")
async def show_children_tariffs(message: types.Message):
    tariffs = await get_tariffs_by_category("дети")
    await send_tariffs(message, tariffs)

@router.message(F.text == "👩‍💼 Уроки для взрослых")
async def show_adult_tariffs(message: types.Message):
    tariffs = await get_tariffs_by_category("взрослые")
    await send_tariffs(message, tariffs)

@router.message(F.text == "🎓 Подготовка к экзаменам")
async def show_exam_tariffs(message: types.Message):
    tariffs = await get_tariffs_by_category("экзамены")
    await send_tariffs(message, tariffs)

# Общая функция отправки тарифов
async def send_tariffs(message: types.Message, tariffs: list):
    if not tariffs:
        await message.answer("Тарифы не найдены для этой категории.")
        return

    for tariff in tariffs:
        text = (
            f"*{tariff['title']}* - {tariff['age_range']}, {tariff['duration_minutes']} минут\n"
            f"_Уровень языка_: {tariff['language_level']}\n"
            f"{tariff['description']}"
        )
        await message.answer(text, parse_mode="Markdown")

    await message.answer("Выбери другую категорию:", reply_markup=tariff_categories_keyboard)


@router.message(F.text == "↩ Вернуться в меню")
async def return_to_main_menu(message: types.Message):
    await message.answer("Вы вернулись в главное меню 😊", reply_markup=get_main_menu(user_id=message.from_user.id))
