import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

TARGET_USER = "PseudoBtw"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == bot.user:
        return

    # Only check webhook messages with embeds
    if message.webhook_id and message.embeds:
        embed = message.embeds[0]  # check the first embed
        title = embed.title or ""
        description = embed.description or ""

        content = (title + " " + description).lower()

        if TARGET_USER.lower() in content:
            try:
                await message.delete()
                print(f"Deleted webhook message containing {TARGET_USER}")
            except discord.Forbidden:
                print("Missing permissions to delete message.")
            except discord.HTTPException as e:
                print(f"Failed to delete message: {e}")

    # Process commands (like !ping)
    await bot.process_commands(message)

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("Error: DISCORD_TOKEN environment variable not set.")
    else:
        bot.run(token)
