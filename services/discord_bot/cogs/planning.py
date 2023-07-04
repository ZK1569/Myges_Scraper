import settings
from discord.ext import commands
import mongo
import service.scraper.schedule as scraper
import service.googleCalendar.googleCalendarApi as googleCalendar

from CustomExceptions.scraperException import idOrPasswordIncorrect, scheduleShowError

class Planning(commands.Cog):

    def __init__(self, bot): 
        self.bot = bot
        self.db = mongo.MongoConnect()
        self.calendarApi = googleCalendar.CalendarAPI()

    
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

        spider = scraper.ScraperSchedule()
        await ctx.send("I'm going to look, just a moment ...")

        try:
            schedule = await spider.getPlanning(myGesId, password)

            if settings.IS_CALENDAR_ENABLED_FOR_OTHERS or ctx.author.name == "zk1569":
                print(settings.IS_CALENDAR_ENABLED_FOR_OTHERS, ctx.author.name == "zk1569")
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
        
    @commands.command()
    async def today(self, ctx):
        """

        """

        cours = self.calendarApi.getTodayEvents()
        [await ctx.send(lesson) for lesson in cours]

async def setup(bot):
    await bot.add_cog(Planning(bot))