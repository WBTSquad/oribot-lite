from tools.mcsrv import mcsrv
from bs4 import BeautifulSoup

from ipwhois import IPWhois

import socket
import requests

import re


def desc():
    return "start servers40 scraping"


def register(bot, logger):
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
                            registrar = '~~`' + registrar + '`~~ ' + ' » `' + \
                                        IPWhois(mcsrvdata['ip']).lookup_whois()["nets"][0]['description'] + '`'
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
                    # b.append(':red_circle: `' + id + '` **::** `' + hostip + '`')
            if i % 10 == 0:
                await ctx.send('\n'.join(b))
                b.clear()
        if c > 0:
            await ctx.send('**(Ori-info)** Were found `' + str(c) + '` server(s) offline!')
        if len(f) > 0:
            # await ctx.send('**(Ori-task)** Generando archivo de información... (vealo local, porque cuando lo subo tira 8000 mil errores :u)')
            file = open(r'servers40.txt', 'w')
            for item in f:
                file.write("%s\n" % item)
            file.close()
            # await ctx.message.channel.send(file=bot.File(open(r'servers40.txt', 'r'), 'whois-info-servers40.txt'))
