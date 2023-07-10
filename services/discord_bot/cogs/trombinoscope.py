import settings 
import service.scraper.trombinoscope as scraper
import mongo

import discord
from discord.ext import commands 
from Models.pagination import PaginationStudentView

logger = settings.logging.getLogger("bot")

class Trombinoscope(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = mongo.MongoConnect()

    @commands.command()
    async def classe(self, ctx):
        """
            Show all your classmates
        """
        students = self.db.getAllStudents()

        pagination_view = PaginationStudentView()
        pagination_view.data = students
        await pagination_view.send(ctx)


    @commands.command()
    async def search(self, ctx):
        """
            Scrape myGes for the last updates
        """
        userId = ctx.author.id
        myGesId = ""
        password = ""
        if self.db.isUserSaved(userId):
            myGesId, password = self.db.getUserLogin(userId)
        else:
            await ctx.send("PTDR T KI ?")
            return 
        
        spider = scraper.ScraperTrombinoscope()
        await ctx.send("I'm looling for ...")

        students = await spider.getTrombinoscope(myGesId, password)

        [await ctx.send(student.first_name, student.last_name) for student in students]
        return 

    @commands.command()
    async def who(self, ctx, name):
        """
            Show the classmate required
        """

        student = self.db.findStudent(name)
        if not student: 
            await ctx.send("I don't know him")
            return 
        
        embed = discord.Embed(color=discord.Color.blue())
        embed.add_field(name=student.last_name, value=student.first_name, inline=False)
        embed.set_image(url=student.image)
        
        await ctx.send(embed=embed)

    
async def setup(bot):
    await bot.add_cog(Trombinoscope(bot))