import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, update
from config import BOT_TOKEN
from db import create_pool
from handlers import start, help, tariffs, register, reminders, schedule, admin, update_data, admin_actions, feedback  # Импортируем роутер с /start
from scheduler.reminders import send_reminders
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from loader import bot, dp

async def main():
    # Инициализация бота и диспетчера -> перенесана в отдельный файл loader
    #bot = Bot(token=BOT_TOKEN)
    #dp = Dispatcher()

    # Подключение к БД
    pool = await create_pool()
    print("✅ База данных подключена")

    # Регистрация всех роутеров
    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(tariffs.router)
    dp.include_router(register.router)
    dp.include_router(reminders.router)
    dp.include_router(schedule.router)
    dp.include_router(admin.router)
    dp.include_router(update_data.router)
    dp.include_router(admin_actions.router)
    dp.include_router(feedback.router)

    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Помощь и инструкция"),
        BotCommand(command="tarifs", description="Узнать тарифы"),
        BotCommand(command="remind_me", description="Настроить напоминание")
    ])

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_reminders, IntervalTrigger(seconds=60), args=[bot])
    scheduler.start()

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
