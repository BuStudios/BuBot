import discord
from dotenv import load_dotenv
import os

load_dotenv() #loads the secret files
bot_token = os.environ["BOT_TOKEN"]
guild_id = os.environ["GUILD_ID"]

bot = discord.Bot()

#logging in msg
@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")

#test command
@bot.slash_command(guild_ids=[guild_id])
async def hello(ctx):
    await ctx.respond(f"Hello {ctx.author.name}!")

#for getting the active developer badge
@bot.slash_command(guild_ids=[guild_id])
async def active_dev(ctx):
    await ctx.respond("https://discord.com/developers/active-developer")

#runs the bot
bot.run(bot_token)