from discord.ext import commands
import mongo
import scraper.schedule
import googleCalendar.googleCalendarApi

from CustomExceptions.scraperException import idOrPasswordIncorrect, scheduleShowError

class Planning(commands.Cog):

    def __init__(self, bot): 
        self.bot = bot
        self.db = mongo.MongoConnect()
        self.calendarApi = googleCalendar.googleCalendarApi.CalendarAPI()

    
    @commands.command()
    async def planning(self, ctx):
        """
            Go to MyGes to get your schedule
        """

        userId = ctx.author.id
        myGesId = ""
        password = ""
        if self.db.isUserSaved(userId):
            myGesId, password = self.db.getUserLogin(userId)
        else:
            await ctx.send("PTDR T KI ?")
            return 

        spider = scraper.schedule.ScraperSchedule()
        await ctx.send("I'm going to look, just a moment ...")

        try:
            schedule = await spider.getPlanning(myGesId, password)
            
            if self.calendarApi.getWeekEvents(*self.calendarApi.intervalDateWeek(schedule)) <= 7:
                self.calendarApi.newEvent(schedule)
            [await ctx.send(lesson) for lesson in schedule]
        except idOrPasswordIncorrect:
            await ctx.send("Your password or Id is incorrect")
            return
        except scheduleShowError:
            await ctx.send("I can't get access to you schedule")
            return 
        except:
            await ctx.send("I didn't succeed, I stumbled ... ")
            return
        
async def setup(bot):
    await bot.add_cog(Planning(bot))