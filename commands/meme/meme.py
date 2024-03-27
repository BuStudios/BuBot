import discord
import json
import requests

async def meme(ctx):
    # meme api
    meme = json.loads(requests.get("https://meme-api.com/gimme/memes").text)
    meme_image = meme["preview"][-1]
    meme_title = meme["title"]
    
    embed = discord.Embed(title=meme_title)
    embed.set_image(url=meme_image)

    # doesnt allow nsfw content
    if meme["nsfw"] == True:
        await ctx.respond("error")
    else:
        await ctx.respond(embed=embed)