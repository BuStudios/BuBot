import discord
from discord.commands import Option
import common.emojis

async def ban(ctx, member: Option(discord.User, "Select a member to ban", required=True), reason: Option(str, "Reason for the ban", required=False) = ""): # type: ignore
    if member.id == ctx.bot.user.id:
        await ctx.respond(f"Why would you want to ban me? {common.emojis.sad_turtle}")
        return

    try:
        await member.ban(reason=reason)
        await ctx.respond(f"{common.emojis.yes} Banned <@{member.id}>! {reason}")

    except discord.Forbidden:
        await ctx.respond(f"I don't have permission to ban this member. Are they Admin? {common.emojis.hmmm}")

    except Exception as e:
        await ctx.respond(f"{common.emojis.error} An error occured while banning <@{member.id}>: `{e}`", ephemeral=True)