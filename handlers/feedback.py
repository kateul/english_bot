from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_IDS

router = Router()

class FeedbackState(StatesGroup):
    waiting_for_feedback = State()

@router.message(F.text == "✉️ Обратная связь")
async def start_feedback(message: types.Message, state: FSMContext):  # ← добавили state
    await message.answer(
        "Тут вы можете оставить свой отзыв об обучении, а также дать свой ✨feedback✨ об уроках.\n"
        "Просто напишите сообщение в чат, и преподаватель его получит ✉️ "
    )
    await state.set_state(FeedbackState.waiting_for_feedback)

@router.message(FeedbackState.waiting_for_feedback)
async def receive_feedback(message: types.Message, state: FSMContext):
    for admin_id in ADMIN_IDS:
        await message.bot.send_message(
            admin_id,
            f"👤 *Имя ученика:* {message.from_user.full_name}\n"
            f"💬 *Сообщение:*\n{message.text}",
            parse_mode="Markdown"
        )

    await message.answer("✅ Спасибо! Ваше сообщение отправлено преподавателю.")
    await state.clear()
