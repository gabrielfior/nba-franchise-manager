from loguru import logger

from Singleton import SingletonMeta

logger.add("nba-franchise-manager.log", rotation="500 MB", backtrace=True)


class Logger(metaclass=SingletonMeta):
    def __init__(self):
        self.logger = logger
