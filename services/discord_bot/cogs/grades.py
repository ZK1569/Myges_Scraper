import discord 
import mongo

from discord.ext import commands
import service.scraper.grades as scraper

from CustomExceptions.scraperException import idOrPasswordIncorrect, scheduleShowError


class Grades(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = mongo.MongoConnect()


    @commands.command()
    async def notes(self, ctx):
        """
            Command to scrap notes from myGes and send data by private message
        """

        userId = ctx.author.id
        myGesId = ""
        password = ""
        if self.db.isUserSaved(userId):
            myGesId, password = self.db.getUserLogin(userId)
        else:
            await ctx.send("PTDR T KI ?")
            return 

        spider = scraper.ScraperGrades()

        try:
            grades = await spider.getGrades(myGesId, password)
            [await ctx.author.send(grade) for grade in grades]
            await ctx.send("Ok it's sent")
        except idOrPasswordIncorrect:
            await ctx.send("Your password or Id is incorrect")
            return
        except Exception as err :
            await ctx.send("I didn't succeed, I stumbled ... ")
            return
        
async def setup(bot):
    await bot.add_cog(Grades(bot))