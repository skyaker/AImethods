import asyncio
from aiogram import Dispatcher
from src.bot.bot import bot, dp
from src.bot.handlers import register_handlers
from src.model.model import load_model

async def main():
	register_handlers(dp)
	await dp.start_polling(bot)

if __name__ == "__main__":
	asyncio.run(main())

# ==============================================================================================================

# from huggingface_hub import InferenceClient

# client = InferenceClient(api_key="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")

# messages = [
# 	{
# 		"role": "user",
# 		"content": "Make a training program for weight loss. User Parameters: Age: 21, Weight: 68, Level: beginner"
# 	}
# ]

# completion = client.chat.completions.create(
# 	model="meta-llama/Meta-Llama-3-8B-Instruct", 
# 	messages=messages, 
# 	max_tokens=1000
# )

# print(completion.choices[0].message)