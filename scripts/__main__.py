from bot.oribot import Oribot
from log.orilog import init_logger

import configparser

# Basic logging initialization
logger = init_logger(__name__, testing_mode=False)


def _main():
    logger.info('Starting the basic setup procedure...')

    '''
    Read the ini config
    for the custom attributes
    '''
    config = configparser.ConfigParser()
    config.read('../config/config.ini')

    '''
    New oribot instance and
    login.
    '''
    clientBot = Oribot(config, logger)
    clientBot.start()


if __name__ == '__main__':
    _main()
