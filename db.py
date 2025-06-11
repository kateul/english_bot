import asyncpg
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


# создаём пул соединений с базой данных
async def create_pool():
    return await asyncpg.create_pool(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


async def add_student(pool, telegram_id, first_name, last_name, day_of_week, lesson_time):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO students (telegram_id, first_name, last_name, day_of_week, lesson_time)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (telegram_id) DO NOTHING
        """, telegram_id, first_name, last_name, day_of_week, lesson_time)

#данный пул создаётся локально внутри функции те это временный пул, и он используется только один раз.
#После выполнения запроса он должен быть закрыт, чтобы не держать открытые соединения с БД.
from datetime import datetime, time

async def update_student_field(user_id: int, field: str, value):
    # Автоматическое преобразование времени из строки в datetime.time
    if field == "lesson_time" and isinstance(value, str):
        try:
            value = datetime.strptime(value.strip(), "%H:%M").time()
        except ValueError:
            raise ValueError("Неверный формат времени. Ожидается 'ЧЧ:ММ'.")

    pool = await create_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            f"UPDATE students SET {field} = $1 WHERE telegram_id = $2",
            value, user_id
        )
    await pool.close()



async def get_student_by_id(telegram_id: int):
    pool = await create_pool()
    async with pool.acquire() as conn:
        return await conn.fetchrow(
            "SELECT * FROM students WHERE telegram_id = $1",
            telegram_id
        )


async def get_student_by_day(day: str):
    pool = await create_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT * FROM students
            WHERE day_of_week ILIKE $1
        """, day)
    await pool.close()
    return rows


async def get_all_students():
    pool = await create_pool()
    async with pool.acquire() as conn:
        return await conn.fetch("SELECT telegram_id, first_name, last_name, day_of_week, lesson_time FROM students")
    await pool.close()


async def get_tariffs_by_category(category: str):
    pool = await create_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM tariffs WHERE category = $1", category)
    await pool.close()
    return rows