from ipwhois import IPWhois


def desc():
    return "start a ip whois"


def register(bot, logger):
    @bot.command()
    async def ipwhois(ctx, ip: str):
        obj = IPWhois(ip)
        res = obj.lookup_whois()
        await ctx.send(res["nets"][0]['description'])
