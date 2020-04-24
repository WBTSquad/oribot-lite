from ipwhois import IPWhois
from tools.scan import syn_silent_scan

import shlex
import nmap
import requests
import discord
import subprocess

nmScan = nmap.PortScanner()


# [Common Ports Cmd]
# This command
# works well but need
# some modifications
common_cmd = 'nmap -p 1-7,2000-2010,3000-3010,4000-4005,20000-20010,20100,20200,20300,20400,20500,20600,20700,20800,20900,21000,21001-21005,21100,21200,21300,21400,21500,21600,21700,21800,21900,22100,22200,22300,22400,22500,22600,22700,22800,22900,23000,23100,23200,23300,23400,23500,23600,23700,23800,23900,24000,24100,24200,24300,24400,24500,24600,24700,24800,24900,27100,27200,27300,27400,27500,27600,27700,27800,27900,28100,28200,28300,28400,28500,28600,28700,28800,28900,29100,29200,29300,29400,29500,29600,29700,29800,29900,60000-60010,10100,10200,10300,10400,10500,10600,10700,10800,10900,11100,11200,11300,11400,11500,11600,11700,11800,11900,12100,12200,12300,12400,12500,12600,12700,12800,12900,13000,13100,13200,13300,13400,13500,13600,13700,13800,13900,14000,14100,14200,14300,14400,14500,14600,14700,14800,14900,15000,15100,15200,15300,15400,15500,15600,15700,15800,15900,16100,16200,16300,16400,16500,16600,16700,16800,16900,17100,17200,17300,17400,17600,17800,17900,18100,18200,18300,18400,18500,18600,18700,18800,18900,19100,19200,19300,19400,19500,19600,19700,19800,19900,30000-30010,25555,25000-25010,25100,25200,25300,25400,25600,25700,25800,25900,26000-26005,40000-40010,10000-10050,50000-50005,11000-11005,65534,65535, -T5 --open %s'


# [Complete Scan]
# It can be slow
all_cmd = 'nmap -p 1-65535, -T5 --open %s'


def desc():
    return "get a lot of information"


def register(bot, logger):
    @bot.command()
    async def complete(ctx, host: str):
        endpoint = 'https://api.mcsrvstat.us/2/'
        await ctx.send('**(Ori-task)** Getting information with MCSRV of `%s`...' % host)
        url = endpoint + host
        resp = requests.get(url=url)
        data = resp.json()
        await ctx.send('> 📣 **IP:** %s\t🔗 **Port:** %s' % (data['ip'], data['port']))
        hostname = host
        if 'hostname' in data:
            hostname = data['hostname']
        await ctx.send('> 🖋 **Host:** %s\t♾ **Online:** %s' % (hostname, data['online']))
        if data['online']:
            await ctx.send(
                '**(Ori-task)** Getting Minecraft information of `%s:%s`...' % (data['ip'], data['port']))
            players = '`(' + str(data['players']['online']) + '/' + str(data['players']['max']) + ')`'
            embed = discord.Embed(title="Server Information", description="")
            embed.add_field(name='⚒ Minecraft Server API', value=data['version'])
            embed.add_field(name='👥 Players', value=players)
            embed.color = discord.Colour.from_rgb(r=247, g=38, b=10)
            await ctx.send(embed=embed)
            await ctx.send(
                '**(Ori-test)** Making pentesting throught `%s`...' % data['ip'])
            await ctx.send(
                ' **»** Getting whois...')
            ip = data['ip']
            obj = IPWhois(ip)
            res = obj.lookup_whois()
            await ctx.send(
                ' **»** Analyzing typical ports...')
            cmd = common_cmd % ip
            args = shlex.split(cmd)
            output = subprocess.check_output(args)
            vulnerabilities = []
            for line in output.split(b'\n'):
                if b'tcp' in line:
                    vulnerabilities.append(line.decode('utf-8'))
            embed_pen = discord.Embed(title="Basic Pentesting Information", description="", color=discord.Colour.from_rgb(r=20, g=249, b=252))
            embed_pen.add_field(name='🔍 Whois', value=res["nets"][0]['description'])
            embed_pen.add_field(name='💢 Ports', value='\n'.join(vulnerabilities))
            await ctx.send(embed=embed_pen)


def as_list(x):
    if type(x) is list:
        return x
    else:
        return [x]


class ThreadScan:
    def __init__(self):
        pass

    def __init__(self, ctx, host):
        self.ctx = ctx
        self.host = host
        pass

    def threaded_scan(self, *values):
        syn_silent_scan(self.ctx, self.host, values)
