import discord
from discord.commands import Option
import datetime
import common.emojis

async def timeout(ctx, member: Option(discord.User, "Select a member to time out", required=True), time: Option(str, "How long should the user be timed out?", required=True), reason: Option(str, "Reason for the timeout", required=False)): # type: ignore
    if member.id == ctx.bot.user.id:
        await ctx.respond(f"Why would you want to time me out? {common.emojis.sad_turtle}")
        return

    try:
        await member.timeout_for(datetime.timedelta(minutes=1))
        await ctx.respond(f"{common.emojis.yes} Timed out <@{member.id}> for 1 minute! {reason}")

    except discord.Forbidden:
        await ctx.respond(f"I don't have permission to timeout this member. Are they Admin? {common.emojis.hmmm}")

    except Exception as e:
        await ctx.respond(f"{common.emojis.error} An error occured while timing out <@{member.id}>: `{e}`", ephemeral=True)