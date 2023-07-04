from time import sleep
import asyncio

from service.scraper.scrape import Scraper
from selenium.webdriver.common.by import By

from typing import List
from Models.gradesModel import GradesModel

class ScraperGrades(Scraper):
    
    def __init__(self):
        super().__init__("https://myges.fr/student/marks")
    
    async def getGrades(self, id, password):
        """
            Run the scraper, start it and stop it
        """
        self.runPage()
        self.LoginPage(id, password)

        grades = self.searchGrades()
        
        self.closePage()

        return grades
    
    def getHeaderTable(self):
        """
            Get from the grades page the header of the table
            
            Return a Dict
        """

        header = self.driver.find_element(By.ID, "marksForm:marksWidget:coursesTable_head").text.split()

        return GradesModel(
            header[0],
            header[1],
            header[2],
            header[3],
            [ s for s in header[4:]]
        )
    

    def searchGrades(self)->List[GradesModel]:
        """
            Main function that reserch notes from the myGes page

            Return an Array[dict]:
                [0] -> Is the header witch 
                [1:] -> Are all the grades by cours subject
        """
        answer = [self.getHeaderTable()]
        
        gradesTable = self.driver.find_element(By.ID, "marksForm:marksWidget:coursesTable_data")

        tableLignes = gradesTable.find_elements(By.CLASS_NAME, 'ui-widget-content')

        for i in tableLignes:
            f = i.find_elements(By.XPATH, ".//*")

            answer.append(GradesModel(
                f[0].text,
                f[2].text,
                f[4].text,
                f[5].text,
                [ s.text for s in f[6:]]
            ))


        return answer



if __name__ == "__main__":
    spider = ScraperGrades()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.getPlanning())
