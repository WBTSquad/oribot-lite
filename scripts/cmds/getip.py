import socket


def desc():
    return "getip from a host"


def register(bot, logger):
    @bot.command()
    async def getip(ctx, host: str):
        await ctx.send('**(Ori-task)** Getting ip of `%s`...' % host)
        await ctx.send('📣 **IP:** %s' % socket.gethostbyname(host))
