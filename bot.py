import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import Command
import aiosqlite
import os

API_TOKEN = os.getenv("BOT_TOKEN")
DATABASE = "data.db"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Setup DB
async def init_db():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS fee_rates (
                group_id INTEGER PRIMARY KEY,
                general REAL DEFAULT 1.0,
                inr REAL DEFAULT 1.0,
                usdt REAL DEFAULT 1.0
            )
        ''')
        await db.commit()

async def set_fee_rate(group_id: int, general=None, inr=None, usdt=None):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''
            INSERT INTO fee_rates (group_id, general, inr, usdt)
            VALUES (?, COALESCE(?, 1.0), COALESCE(?, 1.0), COALESCE(?, 1.0))
            ON CONFLICT(group_id) DO UPDATE SET
                general = COALESCE(?, general),
                inr = COALESCE(?, inr),
                usdt = COALESCE(?, usdt)
        ''', (group_id, general, inr, usdt, general, inr, usdt))
        await db.commit()

async def get_fee_rate(group_id: int):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT general, inr, usdt FROM fee_rates WHERE group_id = ?", (group_id,)) as cursor:
            row = await cursor.fetchone()
            return row if row else (1.0, 1.0, 1.0)

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Hello! I'm your simple escrow bot. Use /help to see available commands.")

@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        "Available Commands:\n"
        "/fee <amount> [rate] - Calculate escrow fee (general)\n"
        "/feeinr <amount> [rate] - Calculate escrow fee in INR (₹)\n"
        "/feeusdt <amount> [rate] - Calculate escrow fee in USDT ($)\n"
        "/setfee <rate> - Set general fee rate\n"
        "/setfeeinr <rate> - Set INR fee rate\n"
        "/setfeeusdt <rate> - Set USDT fee rate\n"
        "/help - Show this message"
    )

@dp.message(Command("fee"))
async def fee_cmd(message: Message):
    try:
        amount = float(message.text.split()[1])
        rate = float(message.text.split()[2]) if len(message.text.split()) > 2 else None
        group_id = message.chat.id
        general, _, _ = await get_fee_rate(group_id)
        fee_rate = rate if rate else general
        fee = (fee_rate / 100) * amount
        total = amount + fee

        result = (
            f"Amount: {amount:.2f}\n"
            f"Fee Rate: {fee_rate}%\n"
            f"Fee: {fee:.2f}\n"
            f"Total: {total:.2f}"
        )

        await message.reply(result)

        try:
            await bot.send_message(message.from_user.id, result)
        except Exception as e:
            logging.warning(f"Failed to DM user {message.from_user.id}: {e}")

    except:
        await message.reply("Usage: /fee <amount> [rate]")

@dp.message(Command("feeinr"))
async def fee_inr(message: Message):
    try:
        amount = float(message.text.split()[1])
        rate = float(message.text.split()[2]) if len(message.text.split()) > 2 else None
        group_id = message.chat.id
        _, inr, _ = await get_fee_rate(group_id)
        fee_rate = rate if rate else inr
        fee = (fee_rate / 100) * amount
        total = amount + fee

        result = (
            f"Amount: {amount:.2f} ₹\n"
            f"Fee Rate: {fee_rate}%\n"
            f"Fee: {fee:.2f} ₹\n"
            f"Total: {total:.2f} ₹"
        )

        await message.reply(result)

        try:
            await bot.send_message(message.from_user.id, result)
        except Exception as e:
            logging.warning(f"Failed to DM user {message.from_user.id}: {e}")

    except:
        await message.reply("Usage: /feeinr <amount> [rate]")

@dp.message(Command("feeusdt"))
async def fee_usdt(message: Message):
    try:
        amount = float(message.text.split()[1])
        rate = float(message.text.split()[2]) if len(message.text.split()) > 2 else None
        group_id = message.chat.id
        _, _, usdt = await get_fee_rate(group_id)
        fee_rate = rate if rate else usdt
        fee = (fee_rate / 100) * amount
        total = amount + fee

        result = (
            f"Amount: {amount:.2f} $\n"
            f"Fee Rate: {fee_rate}%\n"
            f"Fee: {fee:.2f} $\n"
            f"Total: {total:.2f} $"
        )

        await message.reply(result)

        try:
            await bot.send_message(message.from_user.id, result)
        except Exception as e:
            logging.warning(f"Failed to DM user {message.from_user.id}: {e}")

    except:
        await message.reply("Usage: /feeusdt <amount> [rate]")

@dp.message(Command("setfee"))
async def set_fee(message: Message):
    try:
        rate = float(message.text.split()[1])
        await set_fee_rate(message.chat.id, general=rate)
        await message.reply(f"General fee rate set to {rate}%")
    except:
        await message.reply("Usage: /setfee <rate>")

@dp.message(Command("setfeeinr"))
async def set_fee_inr(message: Message):
    try:
        rate = float(message.text.split()[1])
        await set_fee_rate(message.chat.id, inr=rate)
        await message.reply(f"INR fee rate set to {rate}%")
    except:
        await message.reply("Usage: /setfeeinr <rate>")

@dp.message(Command("setfeeusdt"))
async def set_fee_usdt(message: Message):
    try:
        rate = float(message.text.split()[1])
        await set_fee_rate(message.chat.id, usdt=rate)
        await message.reply(f"USDT fee rate set to {rate}%")
    except:
        await message.reply("Usage: /setfeeusdt <rate>")

@dp.my_chat_member()
async def on_new_chat_member(event: ChatMemberUpdated):
    if event.new_chat_member.status == "member":
        await set_fee_rate(event.chat.id)
        await bot.send_message(
            event.chat.id,
            "👋 Hello! I'm your escrow bot.\n"
            "Set your fee rates with /setfee, /setfeeinr, or /setfeeusdt.\n"
            "Use /help to see all commands!"
        )

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
