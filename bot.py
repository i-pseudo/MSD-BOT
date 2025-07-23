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
    if message.author == bot.user:
        return

    print(f"--- Incoming message detected ---")
    print(f"Author: {message.author} | Author ID: {message.author.id}")
    print(f"Content: {message.content}")
    print(f"Webhook ID: {message.webhook_id}")
    print(f"Has embeds: {bool(message.embeds)}")

    if message.webhook_id and message.embeds:
        embed = message.embeds[0]
        title = embed.title or ""
        description = embed.description or ""

        print(f"Embed title: {title}")
        print(f"Embed description: {description}")

        combined_content = (title + " " + description).lower()
        target = TARGET_USER.lower()

        print(f"Looking for '{target}' in '{combined_content}'")

        if target in combined_content:
            try:
                await message.delete()
                print(f"✅ Deleted webhook message containing '{TARGET_USER}'")
            except discord.Forbidden:
                print("❌ Missing permissions to delete message.")
            except discord.HTTPException as e:
                print(f"❌ Failed to delete message: {e}")
        else:
            print("❌ Target string not found in message embeds.")

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("Error: DISCORD_TOKEN environment variable not set.")
    else:
        bot.run(token)
