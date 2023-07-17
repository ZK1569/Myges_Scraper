import settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import settings

from CustomExceptions.scraperException import idOrPasswordIncorrect

logger = settings.logging.getLogger("bot")

class Scraper:
    def __init__(self, url):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(3)
        self.url = url

    def runPage(self):
        logger.info(f"Go on page {self.url}")
        self.driver.get(self.url)

    def waitWillPageContains(self,text, by = By.ID, time: int = 10):
        """
            Waits for the requested element to appear on the screen in 'time' seconds. 

            If after 'time' second the element cannot be found returns false, else returns true
        """
        try:
            WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located((by, text))
            )
            return True
        
        except:
            return False
        
    def doPageContains(self, test, by = By.ID):
        """
            Finds out if an element is on the page

            Return boolean
        """
        try:
            self.driver.find_element(by, test)
            return True
        except:
            return False

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
        if self.waitWillPageContains("username"):    
            self.enterLogin(email, password)
        
            # Check if the password or login is incorrect
            if self.waitWillPageContains("errors", By.CLASS_NAME, 3):
                raise idOrPasswordIncorrect 
        
            # Redirect to the planning page
            self.driver.get(self.url)


        return True
        

    def closePage(self):
        """
            Close the page
        """
        self.driver.quit()