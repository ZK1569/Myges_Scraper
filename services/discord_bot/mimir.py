import discord
from discord.ext import commands
import os 
from dotenv import load_dotenv

import mongo

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!',intents=intents)
db = mongo.MongoConnect()

@client.event
async def on_ready():
    print(f'The bot {client.user} is up')
    print("-"*15)

@client.command()
async def ping(ctx):
    await ctx.send('pong')

@client.command()
async def save(ctx):
    await ctx.send("Functionality is not finished, come back later")

@client.command()
async def me(ctx):
    user_id = ctx.author.id
    user_name = ctx.author.name

    message = f"Your are **{user_name}** and your ID is {user_id} \n \n"
    if(db.isUserSaved(user_id)):
        message += "And I know your myges password and email"
    else:
        message += f"I don't know your password and email \nYou can do the cmd `!save <YOUR EMAIL> <PASSWORD>`"

    await ctx.send(message)

client.run(str(os.getenv('TOKEN')))
