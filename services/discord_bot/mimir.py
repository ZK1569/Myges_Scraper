import discord
from discord.ext import commands
import os 
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()


intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!',intents=intents)

@client.event
async def on_ready():
    print(f'The bot is up {client.user} ')
    print("-"*15)

@client.command()
async def ping(ctx):
    await ctx.send('pong')

client.run(str(os.getenv('TOKEN')))
