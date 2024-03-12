import discord
from dotenv import load_dotenv
import requests
import os

load_dotenv() # loads the secret files
bot_token = os.getenv("BOT_TOKEN") # getenv is better than .environ apparantly
guild_id = os.getenv("GUILD_ID")
# guilds used to add command to a specific server immediatly

intents = discord.Intents.default()
intents.messages = True  # Enables the bot to receive messages
intents.message_content = True  # This is needed for accessing message.content

bot = discord.Bot(command_prefix="!", intents=intents)

response = {
    "sus": "amogus",
    "bustudios": "heleo",
    "bubot": "yes? :robot:",
    "🤖": "hello?" #emoji test
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
    if user_message in ("e", "a"): # imagine using tuples xd
            await message.add_reaction("🇪")
    
    if "rick" in user_message:
        message_rick = ["never", "gonna", "give", "you", "up", "🦀"]
        for msg_rick in message_rick:
            await message.channel.send(msg_rick)

# test command
@bot.slash_command(guild_ids=[guild_id])
async def hello(ctx):
    await ctx.respond(f"Hello {ctx.author.name}!")

@bot.slash_command(guild_ids=[guild_id])
async def website_server(ctx):
    req = requests.get("https://stats.uptimerobot.com/api/getMonitorList/7ryoZuEPWO").json()
    uptime_ratio = req["psp"]["monitors"][1]["90dRatio"]["ratio"]
    today_down = req["psp"]["monitors"][1]["dailyRatios"][0]["ratio"]
    if float(today_down) < 100:
        await ctx.respond("website uptime ratio: " + uptime_ratio + "%\ndowntime detected today: check https://status.bustudios.org/ for more information")
    else:
        await ctx.respond("website uptime ratio: " + uptime_ratio + "%\nno downtime detected today")

# runs the bot
bot.run(bot_token)
