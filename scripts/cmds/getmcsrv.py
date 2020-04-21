import requests
import discord


def desc():
    return "get information via MCSRV"


def register(bot, logger):
    @bot.command()
    async def getmcsrv(ctx, host: str):
        endpoint = 'https://api.mcsrvstat.us/2/'
        await ctx.send('**(Ori-task)** Getting information with MCSRV of `%s`...' % host)
        url = endpoint + host
        resp = requests.get(url=url)
        data = resp.json()
        await ctx.send('> 📣 **IP:** %s\t🔗 **Port:** %s' % (data['ip'], data['port']))
        await ctx.send('> 🖋 **Host:** %s\t♾ **Online:** %s' % (data['hostname'], data['online']))
        if (data['online']):
            await ctx.send(
                '**(Ori-task)** Getting Minecraft information of `%s:%s`...' % (data['ip'], data['port']))
            players = '`(' + str(data['players']['online']) + '/' + str(data['players']['max']) + ')`'
            embed = discord.Embed(title="Server Information", description="")
            embed.add_field(name='⚒ Minecraft Server API', value=data['version'])
            embed.add_field(name='👥 Players', value=players)
            embed.color = discord.Colour.from_rgb(r=247, g=38, b=10)
            await ctx.send(embed=embed)