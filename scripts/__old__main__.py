import re
import discord
import nmap
import whois
import requests
import configparser


from pprint import pprint
from ipwhois import IPWhois
from bs4 import BeautifulSoup
from discord.ext import commands
from scapy.all import *


import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


nmScan = nmap.PortScanner()
description = '''❤ We try to help you.'''
config = configparser.ConfigParser()
config.read('./config/config.ini')
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('¡Summoned Oribot!')
    print('Ori-devs:')
    print(' - Toxic#2381')
    print(' - Wirlie#9272')
    print('Ori-name:', bot.user.name)
    print('Ori-id:', bot.user.id)


@bot.command()
async def ipwhois(ctx, ip: str):
    obj = IPWhois(ip)
    res = obj.lookup_whois()
    await ctx.send(res["nets"][0]['description'])
    #whois_data = whois(ip)
    #print(whois_data.)


@bot.command()
async def sayhello(ctx):
    await ctx.send('Hello! 😁')


@bot.command()
async def servers40(ctx):
    URL = 'https://www.40servidoresmc.es/otrosservidores.php'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.findAll("table", {"class": "tabla-recomen"})
    await ctx.send('**(Ori-task)** Printing results...')
    i = 0
    c = 0
    f = []
    b = []
    for server in results:
        i = i + 1
        online = server.find("img", {"class": "tooltipped icono movil-no"})
        if online != None:
            hostip = server.find("input", {"type": "text"})['value']
            id = server.find("td", {"class": "celda-n"}).string
            registrar = None
            try:
                ip = socket.gethostbyname(hostip)
                bwhois = IPWhois(ip)
                try:
                    registrar = bwhois.lookup_whois()["nets"][0]['description']
                    if re.search('Cloudflare', registrar, re.IGNORECASE):
                        mcsrvdata = await mcsrv(hostip)
                        registrar = '~~`' + registrar + '`~~ ' + ' » `' + IPWhois(mcsrvdata['ip']).lookup_whois()["nets"][0]['description'] + '`'
                    else:
                        registrar = '`' + registrar + '`'
                except:
                    pass
            except:
                pass
            if registrar == None:
                registrar = 'Unknow'
            if online['data-tooltip'] == "Online":
                b.append(':small_blue_diamond: `' + id + '` **::** `' + hostip + '`' + ' **::** ' + registrar)
                f.append(hostip + ' (' + registrar + ')')
            else:
                c = c + 1
                #b.append(':red_circle: `' + id + '` **::** `' + hostip + '`')
        if i % 10 == 0:
            await ctx.send('\n'.join(b))
            b.clear()
    if c > 0:
        await ctx.send('**(Ori-info)** Were found `' + str(c) + '` server(s) offline!')
    if len(f) > 0:
        #await ctx.send('**(Ori-task)** Generando archivo de información... (vealo local, porque cuando lo subo tira 8000 mil errores :u)')
        file = open(r'servers40.txt', 'w')
        for item in f:
            file.write("%s\n" % item)
        file.close()
        #await ctx.message.channel.send(file=bot.File(open(r'servers40.txt', 'r'), 'whois-info-servers40.txt'))


async def mcsrv(host):
    endpoint = 'https://api.mcsrvstat.us/2/'
    url = endpoint + host
    resp = requests.get(url=url)
    data = resp.json()
    return data


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


@bot.command()
async def getip(ctx, host: str):
    await ctx.send('**(Ori-task)** Getting ip of `%s`...' % host)
    await ctx.send('📣 **IP:** %s' % socket.gethostbyname(host))


@bot.command()
async def nmapscan(ctx, ip: str):
    await ctx.send('**(Ori-task)** Scanning (25565-25567) en %s...' % ip)
    nmScan.scan(ip, '25565-25567')  # test 149.56.29.31
    for host in nmScan.all_hosts():
        await ctx.send('🌐 **Host:** %s (`%s`)' % (host, nmScan[host].hostname()))
        await ctx.send('🧩 **State:** %s' % nmScan[host].state().upper())
        for proto in nmScan[host].all_protocols():
            await ctx.send('⸻⸻⸻⸻⸻⸻⸻')  # usando las barras thrid jajaja
            await ctx.send('🧭 **Protocol:** %s' % proto)
            lport = nmScan[host][proto].keys()
            for port in lport:
                await ctx.send('> ◽ Port: `%s`\tState: `%s`' % (port, nmScan[host][proto][port]['state']))


@bot.command()
async def syncscan(ctx, ip: str):
    await ctx.send('**TEST (Ori-task)** Full port scan with tracking (0-65535) en %s...' % ip)
    await syn_scan(ctx, ip, range(0, 65535))


@bot.command()
async def ping(ctx):
    embed = discord.Embed(title="¡POOOOOOONG!", description="\*Poof* The pong arrived and devastated everything in its path 🥊😵")
    embed.color = discord.Colour.from_rgb(r=229, g=52, b=235)
    embed.set_image(url='https://i.pinimg.com/originals/21/02/a1/2102a19ea556e1d1c54f40a3eda0d775.gif')
    await ctx.send(embed=embed)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))


@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')


async def syn_scan(ctx, target, ports):
    print("syn scan on, %s with ports %s" % (target, ports))
    sport = RandShort()
    for port in ports:
        pkt = sr1(IP(dst=target) / TCP(sport=sport, dport=port, flags="S"), timeout=1, verbose=0)
        if pkt != None:
            if pkt.haslayer(TCP):
                if pkt[TCP].flags == 20:
                    sys.stdout.write("~")
                    #print_ports(port, "Closed")
                elif pkt[TCP].flags == 18:
                    print('Opened :: %s:%s' % (target, port))
                    await ctx.send("> ◽ Port: `%s`\tState: `%s`" % (port, 'Opened'))
                else:
                    sys.stdout.write('#')
                    #print_ports(port, "TCP packet resp / filtered")
            elif pkt.haslayer(ICMP):
                sys.stdout.write('&')
                #print_ports(port, "ICMP resp / filtered")
            else:
                sys.stdout.write("?")
                #print_ports(port, "Unknown resp")
                #print(pkt.summary())
        else:
            sys.stdout.write(".")
            #print_ports(port, "Unanswered")


bot.run(config['bot']['token'])