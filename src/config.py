import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMINS_PATH = "admins.txt"
READERS_PATH = "readers.txt"
DB_PATH = os.environ.get("DB_PATH")
TONCENTERAPI = os.environ.get("TONCENTERAPI")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))
API_URL = os.environ.get("API_URL")
