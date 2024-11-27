import asyncio
from aiogram import Dispatcher
from src.bot.bot import bot, dp
from src.bot.handlers import register_handlers

async def main():
	register_handlers(dp)
	await dp.start_polling(bot)

if __name__ == "__main__":
	asyncio.run(main())
