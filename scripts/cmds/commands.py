import os
import imp

import discord


def desc():
    return "show this help message"


def register(bot, logger):
    @bot.command()
    async def commands(ctx):
        cmds = []
        directory = "cmds"
        list_modules = os.listdir(directory)
        list_modules.remove('__loader__.py')
        for module_name in list_modules:
            # add another
            if module_name.split('.')[-1] == 'py':
                cmd = imp.load_source('module', directory + os.sep + module_name)
                desc = 'no information found'
                if hasattr(cmd, 'desc'):
                    desc = cmd.desc()
                cmds.append(':small_blue_diamond: `!' + module_name.split('.')[0] + '` - ' + desc)
        embed = discord.Embed(title="Ori-commands", description="")
        embed.color = discord.Colour.from_rgb(r=94, g=50, b=168)
        embed.description = "\n".join(cmds)
        # embed.set_footer('Oribot v1.02-alpha')
        await ctx.send(embed=embed)