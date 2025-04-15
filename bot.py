import asyncio
from aiogram import Bot, Dispatcher, types
import os
import logging
import threading
from aiohttp import web

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Define your command handlers
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Hello! I'm your escrow bot.")

# Add other handlers as needed...

# Dummy HTTP server to keep Render's Web Service alive
async def handle(request):
    return web.Response(text="Bot is running")

def run_web():
    app = web.Application()
    app.router.add_get("/", handle)
    web.run_app(app, port=10000)

if __name__ == '__main__':
    # Start the dummy web server in a separate thread
    threading.Thread(target=run_web).start()
    
    # Start polling
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
