import discord
import common.reminder_db as reminder_db
from discord.commands import Option
import time
import common.views
import common.emojis

async def set_reminder(ctx, reminder: Option(str, "Reminder reason", max_length=50), timestamp: Option(int, "Reminder Time", name="time")):  # type: ignore

    reminder_time_unix = timestamp + int(time.time())
    reminder_db.add_reminder(reminder_time_unix, ctx.author.name, ctx.author.id, reminder)

    view = common.views.CancelButton(ctx.author.id)

    await ctx.respond(f"{common.emojis.yes} Reminder set! I will remind you <t:{reminder_time_unix}:R>", ephemeral=True, view=view)