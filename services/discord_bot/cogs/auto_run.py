import discord 
import settings
import datetime
from pprint import pprint

import service.googleCalendar.googleCalendarApi as googleCalendar
from discord.ext import commands, tasks



logger = settings.logging.getLogger(__name__)
time = datetime.time(hour=9, minute=55, tzinfo=datetime.timezone.utc)

class AutoRun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dailyPlanning.start()
        self.calendarApi = googleCalendar.CalendarAPI()

    def cog_unload(self):
        self.dailyPlanning.stop()

    @tasks.loop(time=time)
    async def dailyPlanning(self):
        # TODO: Get every day scredule from google calendar
        answer = self.calendarApi.getTodayEvents()
        pprint(answer)

    

async def setup(bot):
    await bot.add_cog(AutoRun(bot))
