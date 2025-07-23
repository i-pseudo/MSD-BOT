import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

TARGET_MESSAGES = [
    "mcslongdong received a",
    "mcslongdong got a pet",
    "mcslongdong found a rare"
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.webhook_id and message.content.strip() in TARGET_MESSAGES:
        try:
            await message.delete()
            print(f"Deleted webhook message: '{message.content}'")
        except discord.Forbidden:
            print("Missing permissions to delete message.")
        except discord.HTTPException as e:
            print(f"Failed to delete message: {e}")

    await bot.process_commands(message)

import os
bot.run(os.getenv("DISCORD_TOKEN"))
