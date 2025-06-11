from aiogram import Router, F, types
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
import asyncpg
from keyboards.inline_reminder import reminder_options
from db import create_pool

router = Router()

async def update_reminder_type(user_id: int, reminder_type: str, enabled: bool=True):
    pool = await asyncpg.create_pool(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE students 
            SET reminders_enabled =  TRUE, reminder_type = $1 
            WHERE telegram_id = $2
        """, reminder_type, user_id)
    await pool.close()


async def update_reminder_flag(user_id: int, flag: bool):
    pool = await asyncpg.create_pool(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE students
            SET reminders_enabled = $1
            WHERE telegram_id = $2
        """, flag, user_id)
    await pool.close()

@router.message(F.text == "🔔 Включить напоминания")
async def choose_reminder_type(message: types.Message):
    await message.answer("Когда напоминать о занятии?", reply_markup=reminder_options)



@router.callback_query(F.data.in_({"reminder_hour", "reminder_day"}))
async def handle_reminder_choice(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    choice = callback.data
    if choice == "reminder_hour":
        await update_reminder_type(user_id, "hour")
        await callback.message.edit_text("⏰ Буду напоминать за 1 час до занятия.")
    elif choice == "reminder_day":
        await update_reminder_type(user_id, "day")
        await callback.message.edit_text("📅 Буду напоминать за 1 день до занятия.")

    await callback.answer()




@router.message(F.text == "🔕 Отключить напоминания")
async def disable_reminders(message: types.Message):
    pool = await asyncpg.create_pool(
        host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE students
            SET reminders_enabled = FALSE, reminder_type = NULL
            WHERE telegram_id = $1
        """, message.from_user.id)

    await pool.close()

    await message.answer("🔕 Напоминания отключены.")