def desc():
    return "send a little hello :)"


def register(bot, logger):
    @bot.command()
    async def sayhello(ctx):
        await ctx.send('Hello! 😁')