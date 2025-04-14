import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Retrieve the bot token from environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Dictionary to store fee rates per group
fee_rates = {}

# Function to calculate fee and total amount
def calculate_fee(amount: float, rate: float):
    fee = round(amount * rate / 100, 2)
    total = round(amount + fee, 2)
    return fee, total

# Function to send fee details to user's private chat
async def send_fee_details_to_user(context: ContextTypes.DEFAULT_TYPE, user_id: int, message: str):
    try:
        await context.bot.send_message(chat_id=user_id, text=message)
    except Exception as e:
        logging.warning(f"Unable to send private message to user {user_id}: {e}")

# Handler for /fee command
async def fee_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /fee <amount> [rate]")
        return

    try:
        amount = float(context.args[0])
        if len(context.args) > 1:
            rate = float(context.args[1])
        else:
            # Use stored rate or default to 4%
            rate = fee_rates.get(update.effective_chat.id, 4.0)

        fee, total = calculate_fee(amount, rate)
        message = (
            f"Amount: {amount:.2f} ₹\n"
            f"Fee Rate: {rate:.1f}%\n"
            f"Fee: {fee:.2f} ₹\n"
            f"Total: {total:.2f} ₹"
        )

        # Send message in group chat
        await update.message.reply_text(message)

        # Send the same message to user's private chat
        user_id = update.effective_user.id
        await send_fee_details_to_user(context, user_id, message)

    except ValueError:
        await update.message.reply_text("Please provide a valid amount and optional rate.")

# Handler for /setfee command
async def setfee_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /setfee <rate>")
        return

    try:
        rate = float(context.args[0])
        fee_rates[update.effective_chat.id] = rate
        await update.message.reply_text(f"Fee rate set to {rate:.1f}% for this group.")
    except ValueError:
        await update.message.reply_text("Please provide a valid rate.")

# Handler for /start command in private chat
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your Escrow Bot. You can use /fee command in group chats to calculate fees, and I'll send you the details here as well.")

# Main function to start the bot
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("fee", fee_command))
    application.add_handler(CommandHandler("setfee", setfee_command))
    application.add_handler(CommandHandler("start", start_command))

    application.run_polling()

if __name__ == "__main__":
    main()
