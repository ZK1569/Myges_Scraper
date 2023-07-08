import pathlib
import os
import logging
import discord
from logging.config import dictConfig
from dotenv import load_dotenv

load_dotenv()

# Docker -------------------------------------------------------------------
MONGO_URL = os.getenv("MONGO_URL")

# Discrord -----------------------------------------------------------------
DISCORD_API_SECRET = os.getenv("TOKEN")
GUILDS_ID = discord.Object(id=int(os.getenv("GUILD")))
HOURE_START = int(os.getenv("HOURE"))
CHANNEL_ID = discord.Object(id=int(os.getenv("CHANNEL"))-2)

# Sraper -------------------------------------------------------------------
IS_CALENDAR_ENABLED_FOR_OTHERS = os.getenv("IS_CALENDAR_ENABLED_FOR_OTHERS")
CALENDAR = os.getenv("CALENDAR")
URL_SCHEDULE = os.getenv("URL_SCHEDULE")
URL_GRADES = os.getenv("URL_GRADES")
URL_CALENDAR = os.getenv("URL_GRADES")

# Others -------------------------------------------------------------------
BASE_DIR = pathlib.Path(__file__).parent
CMDS_DIR = BASE_DIR / "cmds" 
COGS_DIR = BASE_DIR / "cogs" 

# Files --------------------------------------------------------------------
LOGS = os.getenv("LOGS")
GOOGLECREDENTIALS = os.getenv("GOOGLECREDENTIALS")

# Logs ---------------------------------------------------------------------

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(levelname)-10s - %(module)-15s => %(message)s"
        },
        "standard": {
            "format": "%(levelname)-10s %(name)-15s : %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOGS,
            "mode": "w",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "bot": {
            "handlers": ["console", "file"], 
            "level": "INFO", 
            "propagate": False},
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

dictConfig(LOGGING_CONFIG)