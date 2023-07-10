import mongo
import settings

from service.scraper.trombinoscope import ScraperTrombinoscope

logger = settings.logging.getLogger("bot")

class StartBot:
    def __init__(self):
        self.spiderTromb = ScraperTrombinoscope()
        self.db = mongo.MongoConnect()

    async def fillTrombinoscop(self):

        if not self.db.areStudentsSaved():
            print("pas de students")
            answer = self.db.saveStudents(await self.spiderTromb.getTrombinoscope(settings.DEFAULT_USER_NAME, settings.DEFAULT_PASSWORD))
            if answer: logger.info("Student db is initialised")
