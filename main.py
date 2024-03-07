import discord
from dotenv import load_dotenv
import os

load_dotenv()
bot_token = os.environ["BOT_TOKEN"]
guild_id = os.environ["GUILD_ID"]

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[guild_id])
async def hello(ctx):
    await ctx.respond("Hello!")

bot.run(bot_token)