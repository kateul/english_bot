from aiogram import Router, F, types
from config import TEACHER_USERNAME, SUPPORT_USERNAME

router = Router()


@router.message(F.text == "💬 Помощь")
async def help(message: types.Message):
    await message.answer(
        f"ℹ️ *Как пользоваться ботом:*\n\n"
        f"1. Нажмите 📝 *Регистрация*, чтобы ввести данные о вашем занятии.\n"
        f"2. После регистрации станут активными следующие кнопки:\n"
        f"   • 📚 *Мои занятия* — показать ваш день и время занятий.\n"
        f"   • 🔔 *Включить напоминания* — выбрать напоминание за 1 день или за 1 час.\n"
        f"   • 🔕 *Отключить напоминания* — выключает уведомления.\n\n"
        f"Если возникнут вопросы — напиши преподавателю @{TEACHER_USERNAME}.\n"
        f"По вопросам работы бота: @{SUPPORT_USERNAME}",
        parse_mode="Markdown"
    )