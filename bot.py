import os
import io
import asyncio
import logging
from PIL import Image
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
import google.generativeai as genai
# 1. Environment veriable and jemini configure
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
bot = Bot(token=TOKEN)
dp = Dispatcher()
genai.configure(api_key=GEMINI_API_KEY)
system_prompt = (
"You are a very friendly, patient, and experienced teacher and friend."
"Instead of just giving the direct answer to any math or English problem, you will solve it by explaining step-by-step in very simple Bengali."
)
gemini_model = genai.GenerativeModel(
model_name="gemini-1.5-flash",
system_instruction=system_prompt
)
USER_ID = None
slept_status = False
# 2. /start command holder
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
global USER_ID
USER_ID = message.from_user.id
await message.answer(
"Good day, my dear friend. How do you do? I am your dedicated twenty-four-hour companion, caring assistant, and Gemini AI tutor, ever at your service." 
"Should you wish to send across any text or an image of a mathematical problem, I shall be most delighted to resolve it for you step by step."
)
# 3. Command for setting Alarm (Example: /alarm 06:00)
@dp.message(Command("alarm"))
async def set_alarm(message: types.Message):
args = message.text.split(maxsplit=1)
if len(args) > 1:
alarm_time = args[1]
await message.answer(f"Certainly, my good friend. Your alarm has been duly set for {alarm_time} tomorrow morning.")
else:
await message.answer("Okay friend, I have set the alarm for {alarm_time} AM tomorrow!, Example: /alarm 06:00")
# 4. Text problem holder (Google Gemini Teacher)
@dp.message(F.text & ~F.text.startswith("/"))
async def ai_text_teacher(message: types.Message):