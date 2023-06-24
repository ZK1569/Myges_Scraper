from time import sleep
import datetime
import asyncio

from CustomExceptions.scraperException import idOrPasswordIncorrect, scheduleShowError

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SpiderScraper():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)
        self.dates = None

    async def getPlanning(self):
        self.runPage()
        self.LoginPage("cursu", "Jh6AsRRQ")

        self.schoolWeek()

        # Now its on the planning page
        schedule =  self.getDataSchedule()

        self.closePage()

        return schedule

    def runPage(self):
        self.driver.get("https://myges.fr/student/planning-calendar")
    
    def waitWillPageContainsClass(self,text, by = By.ID, time: int = 10):
        try:
            WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located((by, text))
            )
            return True
        
        except:
            return False
        
    def doPageContains(self, test, by = By.ID):
        try:
            self.driver.find_element(by, test)
            return True
        except:
            return False
        
    def schoolWeek(self, iteration = 0):

        if(iteration > 4):
            raise scheduleShowError

        if not self.waitWillPageContainsClass("reservation-NATION1", By.CLASS_NAME, 10):
            print("NO")

            nextweek = self.driver.find_element("id", "calendar:nextMonth")
            nextweek.click()    

            return self.schoolWeek(iteration + 1)
        
        return True
    
    def searchDate(self):
        self.dates = self.driver.find_elements(By.CLASS_NAME, "fc-border-separate")[0].find_elements(By.CLASS_NAME, "ui-widget-header")
    
    def witchDay(self, val):

        if not self.dates : self.searchDate()

        print("date -> ",self.dates[1].text)
        choose = {
            "60px": f"Lundi {self.dates[1].text.split()[1]}", 
            "174px":f"Mardi {self.dates[2].text.split()[1]}", 
            "287px":f"Mercredi {self.dates[3].text.split()[1]}", 
            "400px":f"Jeudi {self.dates[4].text.split()[1]}", 
            "513px":f"Vendredi {self.dates[5].text.split()[1]}", 
            "626px":f"Samedi {self.dates[6].text.split()[1]}"
        }
        return choose[val]

    def getDataSchedule(self):
        courses = self.driver.find_elements(By.CLASS_NAME, "fc-event")
        answer = []

        for cours in courses:
            cours.click()

            self.waitWillPageContainsClass("j_idt174", By.ID, 3)
            # tableNotShow = self.doPageContains("j_idt174", By.ID)

            self.driver.execute_script(
                """document.getElementById('j_idt174').style.top = '0px'; document.getElementById('j_idt174').style.left = '0px'"""
            )
            sleep(1)

            day = self.witchDay(cours.value_of_css_property('left'))

            coursInfos = self.driver.find_elements(By.ID, "dlg1")[0].find_elements(By.TAG_NAME, "tbody")
            # Shearch in coursInfos tbody
            self.waitWillPageContainsClass("matiere", By.ID, 3)
            lesson = {
                "day": day,
                "time": coursInfos[0].find_element(By.ID, "duration").text,
                "matiere": coursInfos[0].find_element(By.ID, "matiere").text,
                "intervenant": coursInfos[0].find_element(By.ID, "intervenant").text,
                "classroom": coursInfos[0].find_element(By.ID, "salle").text,
                "modality": coursInfos[0].find_element(By.ID, "modality").text,

            }
            answer.append(lesson)

        return answer


    def enterLogin(self, email, password):
        """
            Fills the id and password fields of the formulair
        """

        # Find the input and send the email
        email_input = self.driver.find_element("id", "username")
        email_input.send_keys(email)

        # Find the input and send the password
        password_input = self.driver.find_element("id", "password")
        password_input.send_keys(password)


        # Find the button and click on it
        button = self.driver.find_element("name", "submit")
        button.click()
    
    def LoginPage(self, email, password):
        """
            Find out if the site has been redirected to the login page

            If password or login is incorrect, throws idOrPasswordIncorrect error 
            If not return True 
        """

        # Check if the page was redirected to login page
        if self.waitWillPageContainsClass("username"):    
            self.enterLogin(email, password)
        
        # Check if the password or login is incorrect
        if self.waitWillPageContainsClass("errors", By.CLASS_NAME, 3):
            raise idOrPasswordIncorrect 
        
        # Redirect to the planning page
        self.driver.get("https://myges.fr/student/planning-calendar")


        return True
        

    def closePage(self):
        """
            Close the page
        """
        self.driver.quit()
    




if __name__ == "__main__":
    spider = SpiderScraper()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.getPlanning())
    print("FINISHED")



