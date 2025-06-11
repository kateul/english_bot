from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from db import add_student
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from datetime import datetime
import asyncpg
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

# Состояния (этапы диалога)
class RegisterState(StatesGroup):
    first_name = State()
    last_name = State()
    day = State()
    time = State()


#проверка, зарестирован ли уже пользователь
async def is_user_registered(telegram_id: int) -> bool:
    pool = await asyncpg.create_pool(
        host=DB_HOST, port=DB_PORT, database=DB_NAME,
        user=DB_USER, password=DB_PASSWORD
    )
    async with pool.acquire() as conn:
        user = await conn.fetchrow("SELECT * FROM students WHERE telegram_id = $1", telegram_id) #eturns the current row of a recordset as an array
    await pool.close()
    return user is not None

# Старт диалога
@router.message(F.text == "📝 Регистрация")
async def register_start(message: types.Message, state: FSMContext):
    if await is_user_registered(message.from_user.id):
        await message.answer("Ты уже зарегистрирован 😊")
        return

    await message.answer("Как тебя зовут? (Имя)")
    await state.set_state(RegisterState.first_name)

@router.message(RegisterState.first_name)
async def process_first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("А фамилия?")
    await state.set_state(RegisterState.last_name)

@router.message(RegisterState.last_name)
async def process_last_name(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    days_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Понедельник"), KeyboardButton(text="Вторник")],
            [KeyboardButton(text="Среда"), KeyboardButton(text="Четверг")],
            [KeyboardButton(text="Пятница"), KeyboardButton(text="Суббота")],
            [KeyboardButton(text="Воскресенье")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer("В какой день у тебя занятия? (например, Понедельник)", reply_markup=days_keyboard)
    await state.set_state(RegisterState.day)

@router.message(RegisterState.day)
async def process_day(message: types.Message, state: FSMContext):
    await state.update_data(day_of_week=message.text)
    await message.answer("Во сколько начинаются занятия? (в формате HH:MM, время по МСК)")
    await state.set_state(RegisterState.time)

@router.message(RegisterState.time)
async def process_time(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lesson_time = message.text

    try:
        lesson_time = datetime.strptime(lesson_time, "%H:%M").time()
    except ValueError:
        await message.answer("⛔ Неверный формат времени. Введи в формате HH:MM, например 17:30.")
        return

    # Подключаемся к базе (однократно)
    pool = await asyncpg.create_pool(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    await add_student(
        pool=pool,
        telegram_id=message.from_user.id,
        first_name=data["first_name"],
        last_name=data["last_name"],
        day_of_week=data["day_of_week"],
        lesson_time=lesson_time
    )

    await pool.close()

    await message.answer("✅ Ты успешно зарегистрирован!")
    await state.clear()
