from aiogram import Router, F, types
from keyboards.menu import get_main_menu

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: types.Message):
    await message.answer(
        "Привет! Я твой английский помощник 😊. \n\n"
        "Давай познакомимся поближе, для этого тебе нужно зарегистрироваться и ввести свое время занятий, чтобы я мог присылать тебе уведомления о твоих занятиях и актуальные новости.\n\n"
        "Если ты пока что не занимаешься английским, но хочешь начать, то кнопочка тарифы специально для тебя!  ",
        reply_markup=get_main_menu(message.from_user.id)
    )
