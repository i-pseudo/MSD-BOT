import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

TARGET_USER = "McSlongDong"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.webhook_id and message.embeds:
        embed = message.embeds[0]
        title = embed.title or ""
        description = embed.description or ""
        author_name = embed.author.name if embed.author else ""

        combined_content = f"{title} {description} {author_name}".lower()
        target = TARGET_USER.lower()

        if target in combined_content:
            try:
                await message.delete()
            except discord.Forbidden:
                pass  # Bot lacks permission to delete the message
            except discord.HTTPException:
                pass  # Deletion failed for some other reason

    await bot.process_commands(message)

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("Error: DISCORD_TOKEN environment variable not set.")
    else:
        bot.run(token)
