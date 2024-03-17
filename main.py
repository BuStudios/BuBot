import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
import reminder_db
import json
import requests
import time
import os


load_dotenv() # loads the secret files
bot_token = os.getenv("BOT_TOKEN") # getenv is better than .environ apparantly
guild_id = os.getenv("GUILD_ID")
# guilds used to add command to a specific server immediatly
reminder_channel = os.getenv("REMINDER_CHANNEL")


intents = discord.Intents.default()
intents.messages = True  # Enables the bot to receive messages
intents.message_content = True  # This is needed for accessing message.content


bot = discord.Bot(command_prefix="!", intents=intents)


response = {
    "bubot": "amogus",
}


# logging in msg
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    send_message.start()


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


@bot.slash_command(guild_ids=[guild_id], name="meme", description="get memed")
async def meme(ctx):
    # meme api
    meme = json.loads(requests.get("https://meme-api.com/gimme/memes").text)
    meme_image = meme["preview"][-1]
    meme_title = meme["title"]
    
    embed = discord.Embed(title=meme_title)
    embed.set_image(url=meme_image)

    # doesnt allow nsfw content
    if meme["nsfw"] == True:
        await ctx.respond("error")
    else:
        await ctx.respond(embed=embed, ephemeral=True)


@bot.slash_command(guild_ids=[guild_id])
async def reminder(ctx, timestamp: int):

    reminder_time_unix = timestamp + int(time.time())
    reminder_db.add_reminder(reminder_time_unix, ctx.author.name, ctx.author.id)

    await ctx.respond(f"Reminder set! <t:{reminder_time_unix}:R>", ephemeral=True)


@bot.slash_command(guild_ids=[guild_id], name="ping", description="pings the bot")
async def ping(ctx):
    await ctx.respond(f"Pong! The bots latency is {(round(bot.latency * 10) / 10)} ms")


@tasks.loop(seconds=60)
async def send_message():
    due_reminders = reminder_db.check_due_reminders()

    channel = await bot.fetch_channel(reminder_channel)

    for reminders in due_reminders:
        await channel.send(f"Due Reminder for <@{reminders["user_id"]}>")
        reminder_db.delete_reminder(reminders["reminder_id"])


# runs the bot
bot.run(bot_token)