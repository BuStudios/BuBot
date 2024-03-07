import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.commands import Option, slash_command
import os

load_dotenv()
bot_token = os.environ["BOT_TOKEN"]

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx):
    await ctx.respond(f"Hello, world!")

bot.run(bot_token)

#in development