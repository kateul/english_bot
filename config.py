from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
BOT_TOKEN = os.getenv("BOT_TOKEN")

#ADMIN_IDS = os.getenv("ADMIN_IDS")
ADMIN_IDS = set(map(int, os.getenv("ADMIN_IDS", "").split(",")))

TEACHER_USERNAME = os.getenv("TEACHER_USERNAME")
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME")
