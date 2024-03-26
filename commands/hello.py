import discord

async def hello(ctx):
    await ctx.respond(f"Hello {ctx.author.display_name}!")