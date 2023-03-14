import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd

class Review:
    def __init__(self, rating, str_review):
        self.rating = rating
        self.str_review = str_review

class MovieScrapper:
    def __init__(
        self,
        browser: str = "firefox",
        movie: str = None,
        review_number: int = 5,
        _id: str = None,
    ) -> None:
        self.review_number = int(review_number)
        self.key = "k_yna0pgoc"
        match browser:
            case "firefox":
                self.driver = webdriver.Firefox(
                    service=FirefoxService(GeckoDriverManager().install())
                )
            case "chrome":
                self.driver = webdriver.Chrome(
                    service=ChromeService(ChromeDriverManager().install())
                )
            case "chromium":
                self.driver = webdriver.Chrome(
                    service=ChromiumService(
                        ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
                    )
                )
        if not movie and not _id:
            raise ValueError("need id or title")
        self.driver.get(
            f"https://www.imdb.com/title/{_id if _id else self._get_id_from_title(movie)}/reviews"
        )
        self.reviews = self._get_review()
        self.driver.quit()

    def _get_id_from_title(self, movie) -> str:
        """
        to implement in production context.
        Get imdb film id from title (hint : use api)
        - get value for self._id
        return the value
        """
        query = requests.get(
            f"https://imdb-api.com/en/API/SearchMovie/{self.key}/{movie}"
        )
        if query.status_code == 200:
            self.movie_query = query.json()
            return query.json()["results"][0]["id"]
        else:
            raise ReferenceError("something went wrong with the request")

    def _get_review(self) -> list:
        """
        this function return a list of str,
        A single leading underscore before the func name means you're not supposed to access it "from the outside"
        """
        review_list = []
        rating_list = []
        WebDriverWait(self.driver, timeout=10).until(
            lambda d: d.find_element(By.XPATH, "//section[@class='article']")
        )
        self._show_more()
        soup = BeautifulSoup(self.driver.page_source, "html")
        for review in soup.find_all("div", {"class": "review-container"}):
            try:
                stars = (
                    review.find("span", {"class": "rating-other-user-rating"})
                    .find("span")
                    .text
                )
            except:
                stars = None
            str_review = review.find(
                "div", {"class": re.compile("text show-more__control")}
            ).text  # find_element(By.XPATH,"//div[contains(@class,'text show-more__control')]")
            r = Review(stars, str_review)
            #print(r.rating)
            #print(r.str_review)
            review_list.append(r.str_review)
            rating_list.append(r.rating)
            df = pd.DataFrame({"content": review_list, "rating": rating_list})
        return df

    def _show_more(self):
        """be sure the page is loaded before calling this func"""
        number = round(self.review_number / 25)
        while number != 0:
            try:
                WebDriverWait(self.driver, timeout=5).until(
                    lambda d: d.find_element(
                        By.XPATH, "//button[@id='load-more-trigger']"
                    ).click()
                )
                number -= 1
            except:
                break

if __name__ == "__main__":
    import sys

    args = sys.argv
    globals()[args[1]](*args[2:])
