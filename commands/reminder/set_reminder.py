import discord
import common.reminder_db as reminder_db
from discord.commands import Option
import time
import common.views
import common.emojis
from util.timeparser import datetimeParse

async def set_reminder(ctx, reminder: Option(str, "Reminder reason", max_length=50), time_input: Option(str, "Reminder Time", name="time")):  # type: ignore

    timestamp_unix = datetimeParse(time_input)

    if timestamp_unix == "error":
        await ctx.respond(f"{common.emojis.no} Could not parse the time. Use the `10h 5min` format.")

    reminder_db.add_reminder(timestamp_unix, ctx.author.name, ctx.author.id, reminder)

    view = common.views.CancelButton(ctx.author.id)

    await ctx.respond(f"{common.emojis.yes} Reminder set! I will remind you <t:{round(int(timestamp_unix) / 1000)}:R>", ephemeral=True, view=view)