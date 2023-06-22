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
async def save(ctx, email, password):

    # Check if the user has already saved this information 
    if db.isUserSaved:
        await ctx.send("Your information is already saved. If you want to change your password, you can do `!changepassword <YOUR NEW PASSWORD>`")
        return 
    
    # Checks that the user has sent an e-mail and password 
    if not email or not password:
        await ctx.send("You forgot to send me your email and password")
        return 
    
    # Check if the email variable has an @ in it
    if not "@" in email:
        await ctx.send("I'm not strupid, this is not a valid mail ")

    print("Normalement là la personne est pas connue")

    user_id = ctx.author.id

    isSaved = db.saveLogin(user_id, email, password)

    if(isSaved):
        await ctx.send("Thanks for the personal info ...")
        return
    
    await ctx.send("I'm so stupid I couldn't save the information.")
    return

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

@client.command()
async def changepassword(ctx):
    await ctx.send("The functionality is not finished, come back later.")


client.run(str(os.getenv('TOKEN')))
