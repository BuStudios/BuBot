import discord
import common.reminder_db as reminder_db
from discord.commands import Option
import time
import common.views.views

async def set_reminder(ctx, reminder: Option(str, "Reminder reason", max_length=50), timestamp: Option(int, "Reminder Time", name="time")):  # type: ignore
# ^ the Option thing gives an error, but idk why lol --> will change later! ⚠️

    reminder_time_unix = timestamp + int(time.time())
    reminder_db.add_reminder(reminder_time_unix, ctx.author.name, ctx.author.id, reminder)

    view = common.views.views.CancelButton(ctx.author.id)

    await ctx.respond(f"✅ Reminder set! I will remind you <t:{reminder_time_unix}:R>", ephemeral=True, view=view)