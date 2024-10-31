from loguru import logger
import os


LOGGER_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} {level} {name} {function} {line} {message}"
print(os.path.dirname(os.path.realpath(__file__)) + f'/logger/bill_logger.log')
logger.add(
        os.path.dirname(os.path.realpath(__file__)) + f'/bill_logger.log',
        format=LOGGER_FORMAT,
        level='DEBUG',
        rotation='30 MB',
        compression='zip',
        colorize=True
    )
