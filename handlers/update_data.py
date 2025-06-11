from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, State
from db import update_student_field, get_student_by_id
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
from keyboards.update_fields_keyboard import update_fields_keyboard


from keyboards.menu import get_main_menu

router = Router()

class UpdateState(StatesGroup):
    choosing_field = State()
    updating_value = State()


@router.message(F.text == "✏️ Изменить данные")
async def start_update(message: types.Message, state: FSMContext):
    student = await get_student_by_id(message.from_user.id)
    if not student:
        await message.answer("Сначала пройди регистрацию с помощью кнопки 📝 Регистрация.")
        return

    await message.answer(
        f"Твои текущие данные: \n"
        f"Имя: {student['first_name']}\n"
        f"Фамилия: {student['last_name']}\n"
        f"День недели: {student['day_of_week']}\n"
        f"Время занятия: {student['lesson_time']}\n\n"
        f"Что ты хочешь изменить?",
        reply_markup=update_fields_keyboard
    )
    await state.set_state(UpdateState.choosing_field)


@router.message(UpdateState.choosing_field)
async def choose_field(message: types.Message, state: FSMContext):
    if message.text == "🔙 В главное меню":
        await state.clear()
        await message.answer("🏠 Главное меню:", reply_markup=get_main_menu(message.from_user.id))
        return

    field_map = {
        "имя": "first_name",
        "фамилия": "last_name",
        "день": "day_of_week",
        "время": "lesson_time"
    }
    field = field_map.get(message.text.lower())
    if not field:
        await message.answer("Пожалуйста, выбери один из вариантов: Имя / Фамилия / День / Время")
        return

    await state.update_data(field=field)
    await message.answer(f"Введи новое значение для поля «{message.text.capitalize()}»:")
    await state.set_state(UpdateState.updating_value)



@router.message(UpdateState.updating_value)
async def update_value(message: types.Message, state: FSMContext):
    data = await state.get_data()
    field = data["field"]
    value = message.text

    # Преобразуем значение, если это поле времени
    if field == "lesson_time":
        try:
            value = datetime.strptime(value, "%H:%M").time()
        except ValueError:
            await message.answer("⛔️ Неверный формат времени. Введи в формате ЧЧ:ММ (например, 14:30)")
            return

    valid_days = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]

    if field == "day_of_week":
        if value.lower() not in valid_days:
            await message.answer("❌ Укажи корректный день недели, к примеру понедельник, вторник, среда, четверг, пятница, суббота, воскресенье")
            return

    await update_student_field(message.from_user.id, field, value)
    await message.answer("✅ Данные обновлены!\nХочешь изменить что-то ещё?", reply_markup=update_fields_keyboard)
    await state.set_state(UpdateState.choosing_field)


