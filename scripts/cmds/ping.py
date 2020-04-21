import discord


def desc():
    return "little ping"


def register(bot, logger):
    @bot.command()
    async def ping(ctx):
        embed = discord.Embed(title="¡POOOOOOONG!",
                              description="\\*Poof* The pong arrived and devastated everything in its path 🥊😵")
        embed.color = discord.Colour.from_rgb(r=229, g=52, b=235)
        embed.set_image(url='https://i.pinimg.com/originals/21/02/a1/2102a19ea556e1d1c54f40a3eda0d775.gif')
        await ctx.send(embed=embed)
