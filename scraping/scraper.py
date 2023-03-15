from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

class MovieScrapper:

    def __init__(self, browser:str = "firefox", movie: str = None, _id: str = None, review_number: int =5) -> None:
        self.review_number = review_number
        match browser :
            case "firefox" :
                self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
            case "chrome" :
                self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            case "chromium" :
                self.driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
        if _id :
            self.driver.get(f"https://www.imdb.com/title/{_id if _id else self._get_id_from_title()}/reviews")
        self.reviews = self._get_review()
        self.driver.quit()

    def _get_id_from_title(self) -> str :
        """
        to implement in production context.
        Get imdb film id from title (hint : use api)
        - get value for self._id
        return the value
        """
        pass

    def _get_review(self) -> list:
        """
        this function return a list of str,
        A single leading underscore before the func name means you're not supposed to access it "from the outside"
        """
        reviews = []
        ratings = []
        WebDriverWait(self.driver, timeout=10).until(lambda d : d.find_element(By.XPATH,"//section[@class='article']"))
        self._show_more()
        WebDriverWait(self.driver, timeout=2).until(lambda d : d.find_element(By.XPATH,"//div[@class='text show-more__control']"))
        for i in self.driver.find_elements(By.XPATH,"//div[contains(@class,'text show-more__control')]"):
            reviews.append(BeautifulSoup(i.get_attribute("innerHTML"),"lxml").get_text().replace("/"," "))
        for i in self.driver.find_elements(By.XPATH,"//div[contains(@class,'rating-other-user-rating')]"):
            ratings.append(BeautifulSoup(i.get_attribute("innerHTML"),"lxml").get_text().replace("/10",""))

        #list = {"reviews": reviews, "ratings": ratings}
        #df = pd.DataFrame(list)
        return reviews, ratings

    def _show_more(self):
        """be sure the page is loaded before calling this func"""
        number = self.review_number
        while number !=0 :
            try :
                WebDriverWait(self.driver,timeout=5).until(lambda d : d.find_element(By.XPATH, "//button[@id='load-more-trigger']").click())
                number -= 1
            except :
                break

if __name__=="__main__":
    import sys
    args = sys.argv
    globals()[args[1]](*args[2:])
