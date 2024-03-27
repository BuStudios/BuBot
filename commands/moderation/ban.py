import discord
from discord.commands import Option

async def ban(ctx, member: Option(discord.User, "Select a member to ban"), reason: Option(str, "Reason for the ban")): # type: ignore
    try:
        await member.ban(reason=reason)
        await ctx.respond(f"✅ Banned <@{member.id}>! {reason}")
    except Exception as e:
        await ctx.respond(f"an error occured: `{e}`")