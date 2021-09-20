from datetime import datetime
from bs4 import BeautifulSoup as bs
import urllib3
import requests


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Scraper:

    HEAD = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }

    def _get_all(self, pages, website, tags, class_=None):
        self.courses = []
        self.date = datetime.today().strftime("%Y-%m-%d")
        all = []
        for page in range(1, pages + 1):
            response = requests.get(f"{website}{page}", headers=self.HEAD, verify=False)
            soup = bs(response.content, "html5lib")

            if class_:
                all.extend(soup.find_all(*tags, class_=class_))
            else:
                all.extend(soup.find_all(*tags))

        return all

    def _add_course(self, title, link) -> None:
        if not any(d["link"] == link for d in self.courses):
            # link is not repeated
            self.courses.append({"title": title, "link": link, "date": self.date})


class DiscudemyScraper(Scraper):
    def __init__(self, pages):
        super().__init__()
        website = "https://www.discudemy.com/all/"
        tags = ("section", "card")
        self._all = self._get_all(pages, website, tags)

    def find_courses(self) -> None:
        for items in self._all:
            if items.a is None:
                continue
            # Get title
            title = items.a.text
            # Get courses
            url = items.a["href"]
            r = requests.get(url, headers=self.HEAD)
            soup = bs(r.content, "html5lib")
            next = soup.find("div", "ui center aligned basic segment")
            url = next.a["href"]
            r = requests.get(url, headers=self.HEAD)
            soup = bs(r.content, "html5lib")
            link = soup.find("div", "ui segment").a["href"]

            self._add_course(title, link)


class UdemyFreebiesScraper(Scraper):
    def __init__(self, pages):
        super().__init__()
        website = "https://www.udemyfreebies.com/free-udemy-courses/"
        tags = ("div", "theme-block")
        self._all = self._get_all(pages, website, tags)

    def find_courses(self) -> None:
        for items in self._all:
            title = items.img["title"]
            r = requests.get(items.a["href"], headers=self.HEAD, verify=False)
            soup = bs(r.content, "html5lib")
            url = soup.find("a", class_="button-icon")["href"]
            link = requests.get(url, verify=False).url

            self._add_course(title, link)


class TutorialBarScraper(Scraper):
    def __init__(self, pages):
        super().__init__()
        website = "https://www.tutorialbar.com/all-courses/page/"
        tags = ("div", "theme-block")
        class_ = "content_constructor pb0 pr20 pl20 mobilepadding"
        self._all = self._get_all(pages, website, tags, class_)

    def find_courses(self) -> None:
        for items in self._all:
            title = items.a.text
            url = items.a["href"]
            r = requests.get(url)
            soup = bs(r.content, "html5lib")
            link = soup.find("a", class_="btn_offer_block re_track_btn")["href"]

            if "www.udemy.com" in link:
                self._add_course(title, link)
