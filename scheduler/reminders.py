from datetime import datetime, timedelta
from db import create_pool
from aiogram import Bot
import pytz

MOSCOW_TZ = pytz.timezone('Europe/Moscow')

# Словарь для перевода дней недели
EN_TO_RU_DAYS = {
    "Monday": "Понедельник",
    "Tuesday": "Вторник",
    "Wednesday": "Среда",
    "Thursday": "Четверг",
    "Friday": "Пятница",
    "Saturday": "Суббота",
    "Sunday": "Воскресенье",
}

async def send_reminders(bot: Bot):
    now = datetime.now(MOSCOW_TZ)
    day_today_en = now.strftime("%A")
    day_tomorrow_en = (now + timedelta(days=1)).strftime("%A")

    # Переводим на русский
    day_today = EN_TO_RU_DAYS[day_today_en]
    day_tomorrow = EN_TO_RU_DAYS[day_tomorrow_en]

    print(f"⏰ Сейчас: {now.strftime('%Y-%m-%d %H:%M:%S')}, день: {day_today}")

    pool = await create_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT telegram_id, first_name, day_of_week, lesson_time, reminder_type
            FROM students
            WHERE reminders_enabled = TRUE AND day_of_week = ANY($1) AND reminder_type IS NOT NULL
        """, [day_today, day_tomorrow])

        print(f"🔍 Найдено записей: {len(rows)}")

        for row in rows:
            lesson_time = row["lesson_time"]
            reminder_type = row["reminder_type"]

            if reminder_type == "hour" and row["day_of_week"] == day_today:
                lesson_dt = now.replace(
                    hour=lesson_time.hour,
                    minute=lesson_time.minute,
                    second=0,
                    microsecond=0
                )
                delta_minutes = (lesson_dt - now).total_seconds() / 60
                print(f"▶️ {row['first_name']} | Тип: {reminder_type} | lesson_time: {lesson_time}, delta: {delta_minutes:.2f} минут")
                if 59 <= delta_minutes <= 61:
                    await bot.send_message(
                        row["telegram_id"],
                        f'⏰ Привет, {row["first_name"]}! Через 1 час у тебя занятие.'
                    )

            elif reminder_type == "day" and row["day_of_week"] == day_tomorrow:
                if lesson_time.hour == now.hour and lesson_time.minute == now.minute:
                    await bot.send_message(
                        row["telegram_id"],
                        f"📅 Привет, {row['first_name']}! Завтра в {lesson_time.strftime('%H:%M')} у тебя занятие."
                    )

    await pool.close()
