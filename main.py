import discord
from discord.ui.item import Item
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


intents = discord.Intents.default()
intents.messages = True  # Enables the bot to receive messages
intents.message_content = True  # This is needed for accessing message.content


bot = discord.Bot(command_prefix="!", intents=intents)


response = {
    "bubot": "amogus",
}


class ReminderView(discord.ui.View):
    def __init__(self, user_reminders):
        super().__init__()
        self.select_menu = discord.ui.Select(placeholder="Select a reminder to cancel", min_values=1, max_values=1)

        for reminder in user_reminders:
            self.select_menu.add_option(label=reminder["reminder_id"], description=reminder["reason"], value=reminder["reminder_id"])
            
        self.select_menu.callback = self.select_callback
        self.add_item(self.select_menu)

    async def select_callback(self, interaction: discord.Interaction):
        deletion = reminder_db.delete_reminder(self.select_menu.values[0])
        if deletion == "success":
            await interaction.response.send_message(f"✅ The reminder `{self.select_menu.values[0]}` has been canceled!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Could not find the reminder to delete!", ephemeral=True)


class CancelButton(discord.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    @discord.ui.button(label="Cancel Reminder", style=discord.ButtonStyle.danger)
    async def button_callback(self, button, interaction):
        if interaction.user.id == self.user_id:

            button.disabled = True
            await interaction.response.edit_message(view=self)

            await interaction.followup.send("✅ Canceled Reminder!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ You can't cancel someone elses reminder!", ephemeral=True)


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

    await ctx.respond(f"✅ Reminder set! I will remind you <t:{reminder_time_unix}:R>", ephemeral=True, view=CancelButton(ctx.author.id))


@reminder.command(guild_ids=[guild_id], name="list", description="View your reminders")
async def list(ctx):
    user_reminders, reminder_count = reminder_db.get_user_reminders(ctx.author.id)

    if reminder_count == 0:
        await ctx.respond("❌ You don't have any active reminders!", ephemeral=True)
    else:
        embed = discord.Embed(title="Your reminders")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

        reminder_text = "\n".join([f"🔔 `({reminder['reminder_id']})` **{reminder['reason']}** <t:{reminder['timestamp']}:R>" for reminder in user_reminders])

        embed.add_field(name="", value=reminder_text)

        embed.set_footer(text=f"You have {reminder_count} active reminders")

        view = ReminderView(user_reminders)

        await ctx.respond(embed=embed, view=view, ephemeral=True)


@bot.slash_command(guild_ids=[guild_id], name="ban", description="Ban a member")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: Option(discord.User, "Select a member to ban"), reason: Option(str, "Reason for the ban")): # type: ignore
    try:
        await member.ban(reason=reason)
        await ctx.respond(f"banned user <@{member.id}> because of {reason}")
    except Exception as e:
        await ctx.respond(f"an error occured: `{e}`")


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