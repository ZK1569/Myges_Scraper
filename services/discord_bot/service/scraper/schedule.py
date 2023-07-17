from time import sleep
import asyncio
from typing import List
import settings

from CustomExceptions.scraperException import scheduleShowError

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from service.scraper.scrape import Scraper
from Models.oneWeekModel import oneWeekModel

class ScraperSchedule(Scraper):
    """
        This class extends Scrape.py

        Contains all functions related to the search and processing of information found on the myges schedule.
    """
    def __init__(self):

        super().__init__(settings.URL_SCHEDULE)
        self.dates = None

    async def getPlanning(self, id, password):
        self.runPage()
        self.LoginPage(id, password)

        self.schoolWeek()

        schedule =  self.getDataSchedule()

        self.closePage()

        return schedule
        
    def schoolWeek(self, iteration = 0):
        """
            Finds the page with the calendar, if the function loops more than 4 times returns an error scheduleShowError
        """

        if(iteration > 4):
            raise scheduleShowError

        if not self.waitWillPageContains("fc-event-vert", By.CLASS_NAME, 10):

            nextweek = self.driver.find_element("id", "calendar:nextMonth")
            nextweek.click()    

            return self.schoolWeek(iteration + 1)
        
        return True
    
    def searchDate(self):
        """
            Retrieves the dates displayed in the table header from the planning page. 

            This method can only be used if the scraper is on the planning page.
        """
        self.dates = self.driver.find_elements(By.CLASS_NAME, "fc-border-separate")[0].find_elements(By.CLASS_NAME, "ui-widget-header")
    
    def witchDay(self, val):
        """
            Calculates which day of the week the course corresponds to

            Takes card position y in pixels and returns day + date 
        """

        if not self.dates : self.searchDate()

        choose = {
            "60px": f"Lundi {self.dates[1].text.split()[1]}", 
            "174px":f"Mardi {self.dates[2].text.split()[1]}", 
            "287px":f"Mercredi {self.dates[3].text.split()[1]}", 
            "400px":f"Jeudi {self.dates[4].text.split()[1]}", 
            "513px":f"Vendredi {self.dates[5].text.split()[1]}", 
            "626px":f"Samedi {self.dates[6].text.split()[1]}"
        }
        return choose[val]

    def getDataSchedule(self)->List[oneWeekModel]:
        """
            Allows you to retrieve information on the planning cards and more details about them. 

            Returns a dictionary list
        """
        courses = self.driver.find_elements(By.CLASS_NAME, "fc-event")
        answer = []

        for cours in courses:
            cours.click()
            # Waiting for the card with the details to appear 
            self.waitWillPageContains("j_idt176", By.ID, 3)

            # replace the card to avoid a bug
            self.driver.execute_script(
                """document.getElementById('j_idt176').style.top = '0px'; document.getElementById('j_idt176').style.left = '0px'"""
            )
            sleep(1)

            day = self.witchDay(cours.value_of_css_property('left'))

            coursInfos = self.driver.find_elements(By.ID, "dlg1")[0].find_elements(By.TAG_NAME, "tbody")
            # Shearch in coursInfos tbody
            self.waitWillPageContains("matiere", By.ID, 3)

            lesson = oneWeekModel(
                day, 
                coursInfos[0].find_element(By.ID, "duration").text,
                coursInfos[0].find_element(By.ID, "matiere").text,
                coursInfos[0].find_element(By.ID, "intervenant").text,
                coursInfos[0].find_element(By.ID, "salle").text,
                coursInfos[0].find_element(By.ID, "modality").text
            )

            answer.append(lesson)

        return answer


if __name__ == "__main__":
    spider = ScraperSchedule()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.getPlanning())
    print("FINISHED")



