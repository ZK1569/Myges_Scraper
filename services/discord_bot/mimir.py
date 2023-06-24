import os 
import mongo
import scrap
import discord

from discord.ext import commands
from dotenv import load_dotenv

from time import sleep

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
    "Test command"
    await ctx.send('pong')

@client.command()
async def save(ctx, GesId=None, password=None):
    """
        Save your myGes id and password
        Saves the user's information in a database for scrapping his MyGes account.
    """

    user_id = ctx.author.id

    # Check if the user has already saved this information 
    if db.isUserSaved(user_id):
        await ctx.send("Your information is already saved.\nIf you want to change your password, you can do : \n`!changepassword <YOUR NEW PASSWORD>`")
        return 
    
    # Checks that the user has sent an id and password 
    if not GesId or not password:
        await ctx.send("You forgot to send me your mygGes Id and password")
        return 

    isSaved = db.saveLogin(user_id, GesId, password)

    if(isSaved):
        await ctx.send("Thanks for the personal info ...")
        return
    
    await ctx.send("I'm so stupid... I couldn't save the information.")
    return

@client.command()
async def bye(ctx):
    """
        Allows you to delete your password and myGes from the database 
    """

    user_id = ctx.author.id

    # Check if the user has already saved his information 
    if not db.isUserSaved(user_id):
        await ctx.send("I don't know your myGes Id and password")
        return 

    # Delete informations
    # If the response of the function is true or false 
    if db.deleteLogin(user_id):
        await ctx.send("Okay, I'll never use that information again")
        return 


    await ctx.send("I haven't been able to forget your information ")
    return 

@client.command()
async def me(ctx):
    """
        Show your informations

        Enables you to check whether the user who executes the order has his myGes ID and password saved in the database.
    """
    user_id = ctx.author.id
    user_name = ctx.author.name

    message = f"Your are **{user_name}** and your ID is {user_id} \n \n"
    if(db.isUserSaved(user_id)):
        message += "And I know your myges password and id"
    else:
        message += f"I don't know your password and myGes ID \nYou can do the cmd `!save <YOUR ID> <PASSWORD>`"

    await ctx.send(message)

@client.command()
async def changepassword(ctx, password):
    """
        This command changes the password
    """

    await ctx.send("The functionality is not finished, come back later.")

@client.command()
async def planning(ctx):
    """
        Go to MyGes to get your schedule
    """

    userId = ctx.author.id
    myGesId = ""
    password = ""
    if db.isUserSaved(userId):
        myGesId, password = db.getUserLogin(userId)
    else:
        await ctx.send("PTDR T KI ?")
        return 

    spider = scrap.SpiderScraper()
    await ctx.send("I'm going to look, just a moment ...")

    try:
        print(myGesId, password)
        schedul = await spider.getPlanning(myGesId, password)
        [await ctx.send(lesson) for lesson in schedul]
    except scrap.idOrPasswordIncorrect:
        await ctx.send("Your password or Id is incorrect")
        return
    except scrap.scheduleShowError:
        await ctx.send("I can't get access to you schedule")
        return 
    except:
        await ctx.send("I didn't succeed, I stumbled ... ")
        return


client.run(str(os.getenv('TOKEN')))
