import pathlib
import os
import logging
import discord
from logging.config import dictConfig
from dotenv import load_dotenv

load_dotenv()

DISCORD_API_SECRET = os.getenv("TOKEN")
MONGO_URL = os.getenv("MONGO_URL")
IS_CALENDAR_ENABLED_FOR_OTHERS = os.getenv("IS_CALENDAR_ENABLED_FOR_OTHERS")
GUILDS_ID = discord.Object(id=int(os.getenv("GUILD")))

BASE_DIR = pathlib.Path(__file__).parent

CMDS_DIR = BASE_DIR / "cmds" 
COGS_DIR = BASE_DIR / "cogs" 

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "strandard": {
            "format": "%(levelname)-10s - %(name)s : %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            'formatter': 'strandard'
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            'formatter': 'simple'
        },
        "file": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "filename": "logs/infos.log",
            "mode": "w",
            "formatter": "verbose"
        }
    },
    "loggers": {
        "bot": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False
        },
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False
        },

    }
}