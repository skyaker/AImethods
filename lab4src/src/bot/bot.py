import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

token: str = os.getenv('BOT_TOKEN')

if not token:
  raise ValueError("The BOT_TOKEN environment variable is not set. Make sure that the .env file in the src/bot directory contains BOT_TOKEN.")

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)