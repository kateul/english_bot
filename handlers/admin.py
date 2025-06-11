from aiogram import types, F, Router
from aiogram.filters import Command
from config import ADMIN_IDS
from keyboards.admin_menu import get_admin_keyboard

router = Router()


@router.message(F.text == "Админ")
async def admin_panel(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔️ У вас нет доступа к этой команде.")
        return

    await message.answer("🔐 Добро пожаловать в админ-панель!", reply_markup=get_admin_keyboard())


@router.message(F.text == "↩ Назад в админ-панель")
async def back_to_admin_panel(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔️ У вас нет доступа к этой команде.")
        return

    await message.answer("🔐 Вы вернулись в админ-панель.", reply_markup=get_admin_keyboard())