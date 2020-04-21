from tools.scan import syn_scan


def desc():
    return "start a synscan"


def register(bot, logger):
    @bot.command()
    async def syncscan(ctx, ip: str):
        await ctx.send('**(Ori-task)** Full port scan with tracking (0-65535) in %s...' % ip)
        await syn_scan(ctx, ip, range(0, 65535))
