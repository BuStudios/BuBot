import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.commands import Option
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
    check_reminders.start() # Starts the reminder checker


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
    await ctx.respond(f"Hello {ctx.author.display_name}!")


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
        await ctx.respond(embed=embed)


@bot.slash_command(guild_ids=[guild_id], name="ping", description="pings the bot")
async def ping(ctx):
    await ctx.respond(f"Pong! The bots latency is {(round(bot.latency * 10) / 10)} ms")


@bot.slash_command(guild_ids=[guild_id], name="avatar", description="Get a user's avatar")
async def avatar(ctx, user: Option(discord.User, "Select a user", required=False) = None):  # type: ignore
    if user == None:
        user = ctx.author

    embed = discord.Embed()
    embed.set_image(url=user.display_avatar.with_size(256).url)
    embed.set_footer(text=f"Avatar from {user.name}")
    await ctx.respond(embed=embed)


reminder = bot.create_group("reminder", "manage reminders")


@reminder.command(guild_ids=[guild_id], name="set", description="Set a reminder")
async def set(ctx, reminder: Option(str, "Reminder reason", max_length=50), timestamp: Option(int, "Reminder Time", name="time")):  # type: ignore
# ^ the Option thing gives an error, but idk why lol --> will change later! ⚠️

    reminder_time_unix = timestamp + int(time.time())
    reminder_db.add_reminder(reminder_time_unix, ctx.author.name, ctx.author.id, reminder)

    await ctx.respond(f"✅ Reminder set! I will remind you <t:{reminder_time_unix}:R>", ephemeral=True)


@reminder.command(guild_ids=[guild_id], name="list", description="View your reminders")
async def list(ctx):
    user_reminders, reminder_count = reminder_db.get_user_reminders(ctx.author.id)
    if reminder_count == 0:
        await ctx.respond("❌ You don't have any active reminders!")
    else:
        embed = discord.Embed()


# checks if there are any due reminders every 60 seconds
@tasks.loop(seconds=60)
async def check_reminders():
    due_reminders = reminder_db.check_due_reminders()

    for reminders in due_reminders:
        user = await bot.fetch_user(reminders["user_id"]) # fetches the user by their user_id

        dm_channel = await user.create_dm() # creates a dm with the user
        await dm_channel.send(f"🔔 {reminders["reason"]}") # send a dm to the user
        # <@{reminders["user_id"]}> Reminder!

        reminder_db.delete_reminder(reminders["reminder_id"]) # deletes the reminder from the database


# runs the bot
bot.run(bot_token)