import asyncio
import os
import logging
import threading
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher (for aiogram v3)
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# Define your command handlers
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello! I'm your escrow bot.")

# Add other handlers as needed...

# Dummy HTTP server to keep Render's Web Service alive
async def handle(request):
    return web.Response(text="Bot is running!")

def run_web():
    app = web.Application()
    app.router.add_get("/", handle)
    web.run_app(app, port=10000)

# Main entry point
async def main():
    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Start the dummy web server in a separate thread
    threading.Thread(target=run_web).start()
    
    # Run the bot polling
    asyncio.run(main())
