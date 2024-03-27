import discord

async def ping(ctx):
    # Accessing the bot instance through ctx
    bot_latency = round(ctx.bot.latency * 1000, 1)  # Convert to milliseconds and round
    await ctx.respond(f"Pong! The bot's latency is {bot_latency} ms")