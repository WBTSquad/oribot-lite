import imp, os


def __load_all__(bot, logger):
    directory = "cmds"
    list_modules = os.listdir(directory)
    list_modules.remove('__loader__.py')
    for module_name in list_modules:
        if module_name.split('.')[-1] == 'py':
            logger.info("Loading command '" + module_name + "' *")
            cmd = imp.load_source('module', directory + os.sep + module_name)
            cmd.register(bot, logger)
