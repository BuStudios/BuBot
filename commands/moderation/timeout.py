import discord
from discord.commands import Option
import datetime

async def timeout(ctx, member: Option(discord.User, "Select a member to time out"), reason: Option(str, "Reason for the timeout")): # type: ignore
    try:
        await member.timeout_for(datetime.timedelta(minutes=1))
        await ctx.respond(f"✅ Banned <@{member.id}>! {reason}")
    except Exception as e:
        await ctx.respond(f"an error occured: `{e}`")