# (Everything above stays the same...)

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

        # Send DM to user
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

        # Send DM to user
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

        # Send DM to user
        try:
            await bot.send_message(message.from_user.id, result)
        except Exception as e:
            logging.warning(f"Failed to DM user {message.from_user.id}: {e}")

    except:
        await message.reply("Usage: /feeusdt <amount> [rate]")

# (Everything below stays the same...)
