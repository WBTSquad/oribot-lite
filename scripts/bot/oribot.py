from discord.ext import commands

import cmds.__loader__

class Oribot:
  def __init__(self, config, logger):
    logger.info('Initializing oribot instance...')

    self.logger = logger
    self.config = config

    self.description = '''❤ We try to help you.'''
    self.bot = commands.Bot(command_prefix='!', description=self.description)

    logger.info('Loading commands...')
    cmds.__loader__.__load_all__(self.bot, self.logger)

    @self.bot.event
    async def on_ready():
      logger.info('Summoned Oribot!')
      logger.info('Ori-devs:')
      logger.info(' » Toxic#2381')
      logger.info(' » Wirlie#9272')
      logger.info(' » Boogst#6806')
      logger.info('Ori-name: ' + self.bot.user.name)
      logger.info('Ori-id: ' + str(self.bot.user.id))

  def start(self):
    self.logger.info("Starting oribot...")
    self.bot.run(self.config['discord']['token'])
    self.logger.info("Oribot logged in!")