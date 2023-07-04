import discord 
import settings
import datetime
from pprint import pprint

import service.googleCalendar.googleCalendarApi as googleCalendar
from discord.ext import commands, tasks



logger = settings.logging.getLogger("bot")
time = datetime.time(hour=11, minute=52, tzinfo=datetime.timezone.utc)

class AutoRun(commands.Cog):
    def __init__(self, bot: discord.Guild):
        self.bot = bot
        self.dailyPlanning.start()
        self.calendarApi = googleCalendar.CalendarAPI()

    def cog_unload(self):
        self.dailyPlanning.stop()

    @tasks.loop(time=time)
    async def dailyPlanning(self):
        # TODO: Get every day scredule from google calendar
        answer = self.calendarApi.getTodayEvents()
        # This is not working
        # [await channel.send(cours) for cours in answer]
    

async def setup(bot):
    await bot.add_cog(AutoRun(bot))
