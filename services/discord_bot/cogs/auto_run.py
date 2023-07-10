import discord 
import settings
import datetime
from pprint import pprint

import service.googleCalendar.googleCalendarApi as googleCalendar
from discord.ext import commands, tasks



logger = settings.logging.getLogger("bot")
time = datetime.time(hour=9, minute=0, tzinfo=datetime.timezone.utc)

class AutoRun(commands.Cog):
    def __init__(self, bot: discord.Guild):
        self.bot = bot
        self.dailyPlanning.start()
        self.calendarApi = googleCalendar.CalendarAPI()

    def cog_unload(self):
        self.dailyPlanning.stop()

    @tasks.loop(time=time)
    async def dailyPlanning(self):
        """
            Displays the day's courses, if any, every morning
        """
        answer = self.calendarApi.getTodayEvents()
        if answer == []:
            return 
        chanel = self.bot.get_channel(settings.CHANNEL_ID)
        [await chanel.send(f"{lesson.date_start.split()[1]}-{lesson.date_end.split()[1]} | **{lesson.course}** avec {lesson.teacher} || {lesson.classroom}") for lesson in answer]
        logger.info("Today's schedule is shown.")
    

async def setup(bot):
    await bot.add_cog(AutoRun(bot))
