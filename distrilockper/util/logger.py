import logging
import logging.config
from pythonjsonlogger import jsonlogger
import pathlib
import os
import logging.handlers
import datetime
import json
import coloredlogs


logger_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'json': {
            'format': '[%(asctime)s.%(msecs)10f][%(threadName)s:%(thread)d][%(name)s:%(levelname)s:%(lineno)d)]\n[%(module)s:%(funcName)s]:%(message)s\n\n',
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
        },
        'color': {
            '()': 'coloredlogs.ColoredFormatter',
            'format': "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s(): - %(lineno)d: - %(message)s",
            'datefmt' : "%Y-%m-%d %H:%M:%S%Z"
        },

        'standard':{
            'format': "%(asctime)s.%(msecs)03d %(threadName)s %(thread)d %(name)s %(levelname)s %(module)s %(funcName)s() %(lineno)d %(message)s",
            'datefmt' : "%Y-%m-%d,%H:%M:%S%Z"
        }
    },
    'handlers': {
        'file': {
            # new log file pre 10 min, max 30 backup files
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'json',
            'filename': './log/lock_helper.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30
        },
        'standard': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'color_standard': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'json_standard': {
            'level': 'INFO',
            'formatter': 'json',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
    },
    'loggers': {
        'lock_helper': {  # root logger
            'handlers': ['color_standard',"file"],
            'level': 'INFO',
            'propagate': False
        },
        'my.packg': {
            'handlers': ['standard'],
            'level': 'INFO',
            'propagate': False
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['standard'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

class logger_register(object):
    def __init__(self):
        log_folder = str(pathlib.Path().absolute())+"/log"
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        logging.config.dictConfig(logger_config)