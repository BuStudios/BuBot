import discord
from discord.ui.item import Item
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.commands import Option
import common.reminder_db as reminder_db
import json
import requests
import time
import os

import commands as cmds


load_dotenv(dotenv_path="config/.env") # loads the secret files
bot_token = os.getenv("BOT_TOKEN") # getenv is better than .environ apparantly
guild_id = os.getenv("GUILD_ID")
# guilds used to add command to a specific server immediatly


intents = discord.Intents.default()
intents.messages = True  # Enables the bot to receive messages
intents.message_content = True  # This is needed for accessing message.content


bot = discord.Bot(command_prefix="!", intents=intents, activity=discord.CustomActivity("Cookies 🍪"))


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


# COMMANDS

bot.slash_command(guild_ids=[guild_id])(cmds.hello)

bot.slash_command(guild_ids=[guild_id], name="meme", description="get memed")(cmds.meme)

bot.slash_command(guild_ids=[guild_id], name="ping", description="pings the bot")(cmds.ping)

bot.slash_command(guild_ids=[guild_id], name="avatar", description="Get a user's avatar")(cmds.avatar)


reminder = bot.create_group("reminder", "manage reminders")

reminder.command(guild_ids=[guild_id], name="set", description="Set a reminder")(cmds.set_reminder)
reminder.command(guild_ids=[guild_id], name="list", description="View your reminders")(cmds.reminder_list)


bot.slash_command(guild_ids=[guild_id], name="ban", description="Ban a member")(cmds.ban)


# checks if there are any due reminders every 60 seconds
@tasks.loop(seconds=60)
async def check_reminders():
    due_reminders = reminder_db.check_due_reminders()

    for reminders in due_reminders:
        user = await bot.fetch_user(reminders["user_id"]) # fetches the user by their user_id

        dm_channel = await user.create_dm() # creates a dm with the user
        await dm_channel.send(f"🔔 {reminders['reason']}") # send a dm to the user
        # <@{reminders["user_id"]}> Reminder!

        reminder_db.delete_reminder(reminders["reminder_id"]) # deletes the reminder from the database


# runs the bot
bot.run(bot_token)