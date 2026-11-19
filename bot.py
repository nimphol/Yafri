
import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from dotenv import load_dotenv
from google import genai

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TOKEN or not GEMINI_API_KEY:
    raise ValueError("BOT_TOKEN or GEMINI_API_KEY is missing!")

# Initialize bot and Gemini
bot = Bot(token=TOKEN)
dp = Dispatcher()

gemini_client = genai.Client(api_key=GEMINI_API_KEY)

system_prompt = """
You are a very friendly, patient, and experienced teacher.

You are also a helpful friend.

Instead of giving only direct answers to math or English
problems, explain solutions step by step in very simple Bengali.

Make your explanations suitable for students.
"""

# Start command
@dp.message(Command("start"))
async def cmd_start(message: types.Message):

    await message.answer(
        "Good day, my dear friend! How do you do?\n\n"
        "I am Yafri, your dedicated companion and Gemini AI tutor.\n\n"
        "Send me a text question and I will explain "
        "the solution step by step in simple Bengali."
    )


# Alarm command (temporary placeholder)
@dp.message(Command("alarm"))
async def set_alarm(message: types.Message):

    await message.answer(
        "The alarm feature is currently being prepared.\n"
        "It is not activated yet."
    )


# Gemini text tutor
@dp.message(F.text & ~F.text.startswith("/"))
async def ai_text_teacher(message: types.Message):

    question = message.text

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action="typing"
    )

    try:
        prompt = (
            system_prompt
            + "\n\nStudent's question:\n"
            + question
        )

        response = await asyncio.to_thread(
            gemini_client.models.generate_content,
            model="gemini-3.8-flash",
            contents=prompt
        )

        answer = response.text

        if not answer:
            await message.answer(
                "Sorry, I couldn't generate an answer. Please try again."
            )
            return

        # Telegram message limit is 4096 characters
        for i in range(0, len(answer), 4000):
            await message.answer(answer[i:i + 4000])

    except Exception:
        logger.exception("Gemini API error")
        await message.answer(
            "Sorry, something went wrong. Please try again later."
        )


# Run bot
async def main():

    logger.info("Yafri bot is starting...")

    try:
        await dp.start_polling(bot)

    finally:
        await bot.session.close()
        await gemini_client.aio.aclose()


if __name__ == "__main__":
    asyncio.run(main())
