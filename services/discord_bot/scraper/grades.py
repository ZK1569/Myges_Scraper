from time import sleep
import asyncio

from scraper.scrape import Scraper
from selenium.webdriver.common.by import By

from pprint import pprint

class ScraperGrades(Scraper):
    
    def __init__(self):
        super().__init__("https://myges.fr/student/marks")
    
    async def getGrades(self, id, password):
        self.runPage()
        self.LoginPage(id, password)

        grades = self.searchGrades()
        
        self.closePage()

        return grades
    
    def getHeaderTable(self):

        header = self.driver.find_element(By.ID, "marksForm:marksWidget:coursesTable_head").text.split()

        return {
            "matere" : header[0],
            "teatcher": header[1],
            "coef" : header[2],
            "ects" : header[3],
            "grades" : [ s for s in header[4:]]
        }
    

    def searchGrades(self):
        answer = [self.getHeaderTable()]
        
        gradesTable = self.driver.find_element(By.ID, "marksForm:marksWidget:coursesTable_data")

        tableLignes = gradesTable.find_elements(By.CLASS_NAME, 'ui-widget-content')

        for i in tableLignes:
            f = i.find_elements(By.XPATH, ".//*")

            answer.append({
                "matere" : f[0].text,
                "teatcher": f[2].text,
                "coef" : f[4].text,
                "ects" : f[5].text,
                "grades" : [ s.text for s in f[6:]]
            })

        return answer



if __name__ == "__main__":
    spider = ScraperGrades
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.getPlanning())
