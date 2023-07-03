import discord 
import datetime
import mongo
from discord.ext import commands


class HomeWork(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = mongo.MongoConnect()

    @commands.command()
    async def add(self, ctx, date:str, *, args):
        """
            Add a homework

            Required arguments:
                - date: The date of the homework (format: dd/mm/yyyy)
                - args: The homework description
        """
        try:
            day, month, year = date.split("/")
            date = datetime.datetime(int(year), int(month), int(day))
        except:
            await ctx.send("La date est pas bonne")
            return

        if self.db.addHomework(ctx.author.id ,date, args):
            await ctx.send("OK")
            return 
        else:
            await ctx.send("C'est pas save")
    
    @commands.command()
    async def get(self, ctx, date:str):
        """
            Get homeworks

            Required arguments:
                - date: The date of the homework (format: dd/mm/yyyy)
        """

        if not date:
            await ctx.send("T'as pas envoyer de date.")
            return 
        
        try:
            day, month, year = date.split("/")
            date = datetime.datetime(int(year), int(month), int(day))
        except:
            await ctx.send("La date est pas bonne")
            return 
        todo = self.db.getHomework(ctx.author.id, date)

        # if not todo[0]:
        #     await ctx.send("There is no homework for this date")
        #     return

        [await ctx.send(f"Le {str(task['date']).split()[0]} =>  **{task['description']}**") for task in todo]
        return 
    
async def setup(bot):
    await bot.add_cog(HomeWork(bot))