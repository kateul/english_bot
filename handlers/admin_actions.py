from aiogram import types, Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from db import get_student_by_day, get_all_students
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from keyboards.days import days_keyboard
from keyboards.admin_menu import get_admin_keyboard
from loader import bot

router = Router()


class FilterStudents(StatesGroup):
    day = State()


class Broadcast(StatesGroup):
    waiting_for_message = State()


@router.message(F.text == "👥 Список учеников")
async def show_day_filter(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Выбери день недели:", reply_markup=days_keyboard)
    await state.set_state(FilterStudents.day)


@router.message(FilterStudents.day)
async def show_students(message: types.Message, state: FSMContext):
    print(f"[DEBUG] Получен день: {message.text}")
    day = message.text.strip()
    if day == "📅 Вся неделя":
        students = await get_all_students()
    else:
        students = await get_student_by_day(day)

    if not students:
        await message.answer("Ученики не найдены.")
    else:
        text = ""
        for s in students:
            text += f"👤 {s['first_name']} {s['last_name']} — {s['day_of_week']} в {s['lesson_time']}\n"
        await message.answer(text)

    await message.answer("Хочешь посмотреть учеников за другой день?", reply_markup=days_keyboard)

    await state.clear()


@router.message(F.text == "📢 Сделать рассылку")
async def ask_for_broadcast_message(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Напиши сообщение, которое ты хочешь разослать всем ученикам:")
    await state.set_state(Broadcast.waiting_for_message)


@router.message(Broadcast.waiting_for_message)
async def send_broadcast(message: types.Message, state: FSMContext):
    students = await get_all_students()
    count = 0
    for student in students:
        try:
            await bot.send_message(student['telegram_id'], message.text)
            count += 1
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {student.get('telegram_id')}: {e}")
    await message.answer(f"📨 Сообщение отправлено {count} ученикам.", reply_markup=get_admin_keyboard())
    await state.clear()

