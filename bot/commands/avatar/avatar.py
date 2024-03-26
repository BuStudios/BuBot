import discord
from discord.commands import Option

async def avatar(ctx, user: Option(discord.User, "Select a user", required=False) = None):  # type: ignore
    if user == None:
        user = ctx.author

    embed = discord.Embed()
    embed.set_image(url=user.display_avatar.with_size(256).url)
    embed.set_footer(text=f"Avatar from {user.name}")
    await ctx.respond(embed=embed)