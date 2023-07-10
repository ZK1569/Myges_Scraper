import time
import settings
from Models.studentModel import Student
from typing import List

from service.scraper.scrape import Scraper
from selenium.webdriver.common.by import By

class ScraperTrombinoscope(Scraper):

    def __init__(self):
        super().__init__(settings.URL_TROMBINOSCOPE)
    
    async def getTrombinoscope(self, id, password):
        self.runPage()
        self.LoginPage(id, password)

        students = self.searchStudents()

        self.closePage()
        
        return students
    
    def isLastPageTromb(self):

        _ , current_page, _ , last_page = self.driver.find_element(By.CLASS_NAME, "ui-paginator-current").text.split()
        
        return current_page >= last_page
    
    def goNextPageTromb(self):
        btn_next = self.driver.find_element(By.CLASS_NAME, "ui-paginator-next")
        btn_next.click()
    
    def searchStudents(self)->List[Student]:
        allStudents:List[Student] = []
        doLast = True

        while not self.isLastPageTromb() or doLast:
            
            students_in_row = self.driver.find_elements(By.CLASS_NAME, "ui-datagrid-row")
            for students in students_in_row:
                students = students.find_elements(By.CLASS_NAME, "ui-datagrid-column")
                for student in students:
                    if student.text != "":  
                        image = student.find_element(By.XPATH, ".//img").get_attribute("src")
                        last_name, first_name  = student.find_element(By.CLASS_NAME, "mg_directory_text").text.split("\n")
                        allStudents.append(Student(image, first_name, last_name))

            if self.isLastPageTromb():
                doLast = False

            self.goNextPageTromb()
            time.sleep(1)

        return allStudents

