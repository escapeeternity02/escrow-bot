# Simple Telegram Escrow Bot

This is a simple Telegram escrow bot for fee calculations in general, INR, and USDT.

## Features
- Per group fee rate storage
- /fee, /feeinr, /feeusdt commands for fee calculation
- /setfee, /setfeeinr, /setfeeusdt for setting group-specific rates
- Welcome message when added to a group

## Deploy on Render
1. Create a new web service
2. Add environment variable `BOT_TOKEN` with your bot token
3. Deploy from GitHub

## Commands
- `/fee <amount> [rate]` - Calculate escrow fee (general)
- `/feeinr <amount> [rate]` - Calculate escrow fee in INR (₹)
- `/feeusdt <amount> [rate]` - Calculate escrow fee in USDT ($)
- `/setfee <rate>` - Set general fee rate
- `/setfeeinr <rate>` - Set INR fee rate
- `/setfeeusdt <rate>` - Set USDT fee rate
- `/help` - Show help message
