import discord
from dotenv import load_dotenv
import os

load_dotenv() # loads the secret files
bot_token = os.environ["BOT_TOKEN"]
guild_id = os.environ["GUILD_ID"]

intents = discord.Intents.default()
intents.messages = True  # Enables the bot to receive messages
intents.message_content = True  # This is crucial for accessing message.content

# Initialize your bot with the specified intents
bot = discord.Bot(command_prefix="!", intents=intents)

response = {
    "sus": "amogus",
    "bustudios": "heleo",
    "bubot": "yes? :robot:",
    "ban me": "no",
    "e": ":regional_indicator_e:"
}

# logging in msg
@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:  # Ignore messages from bots
        return
    
    user_message = message.content.lower()

    if user_message in response: # Checks if item is in the message
        await message.channel.send(response[user_message])

# test command
@bot.slash_command(guild_ids=[guild_id])
async def hello(ctx):
    await ctx.respond(f"Hello {ctx.author.name}!")

# for getting the active developer badge
@bot.slash_command(guild_ids=[guild_id])
async def active_dev(ctx):
    await ctx.respond("https://discord.com/developers/active-developer")

# runs the bot
bot.run(bot_token)