from aiogram import Router, F, types
import asyncpg #asyncpg is a database interface library designed specifically for PostgreSQ
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

router = Router()

@router.message(F.text == "📚 Мои занятия")
async def show_schedule(message: types.Message):
    pool = await asyncpg.create_pool(
        host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    async with pool.acquire() as conn:
        user = await conn.fetchrow("""
        SELECT first_name, last_name, day_of_week, lesson_time 
        FROM students WHERE telegram_id = $1
        """, message.from_user.id)

    await pool.close()

    if user is None:
        await message.answer("Ты ещё не зарегистрирован. Нажми 📝 Регистрация.")
    else:
        await message.answer(
           f'🗓 Занятия у тебя проходят в *{user["day_of_week"]}*\n' #*...* — способ выделить жирный текст
            f'🕒 Время: *{user["lesson_time"].strftime("%H:%M")}*\n'

            f'👤 Имя: {user["first_name"]}',
            parse_mode='Markdown'

        )