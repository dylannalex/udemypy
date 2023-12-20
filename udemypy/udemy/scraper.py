import re
import urllib3
import requests
from selenium import webdriver
from selenium_stealth import stealth
from bs4 import BeautifulSoup as bs
from abc import ABC
from abc import abstractmethod
from datetime import datetime
from time import sleep

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


"""
_CoursesScraper:

Scrapes Udemy courses links from a free courses website.
"""


class _CoursesScraper(ABC):
    HEAD = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }

    @abstractmethod
    def find_courses(self) -> None:
        pass

    def _get_all(self, pages, website, tags, class_=None):
        self.courses = []
        self.date = datetime.today()
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
        if any(d["link"] == link for d in self.courses):
            # link is repeated
            return
        link_list = link.split("/?")
        course_link = f"{link_list[0]}/"

        try:
            coupon_code = link_list[1].split("=")[1]
        except IndexError:
            # Could not find course coupon
            return

        self.courses.append(
            {
                "title": title,
                "link": course_link,
                "coupon_code": coupon_code,
                "date_found": self.date,
            }
        )


class DiscudemyScraper(_CoursesScraper):
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


class UdemyFreebiesScraper(_CoursesScraper):
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


class TutorialBarScraper(_CoursesScraper):
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
            class_ = soup.find("a", class_="btn_offer_block re_track_btn")
            if class_:
                link = class_["href"]
            if "www.udemy.com" in link:
                self._add_course(title, link)


"""
StatsScraper:
Scrape Udemy course statistics (rating, students, etc).
"""


class StatsScraper:
    SLEATH_SETTINGS = {
        "languages": ["en-US", "en"],
        "vendor": "Google Inc.",
        "platform": "Win32",
        "webgl_vendor": "Intel Inc.",
        "renderer": "Intel Iris OpenGL Engine",
        "fix_hairline": True,
    }

    def __init__(
        self, chromedriver_path: str, google_chrome_bin: str, page_load_time: int
    ):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("log-level=3")
        options.add_argument("--disable-gpu")
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        if google_chrome_bin:
            options.binary_location = google_chrome_bin
        self.driver = webdriver.Chrome(
            options=options, executable_path=chromedriver_path
        )
        stealth(
            self.driver,
            languages=StatsScraper.SLEATH_SETTINGS["languages"],
            vendor=StatsScraper.SLEATH_SETTINGS["vendor"],
            platform=StatsScraper.SLEATH_SETTINGS["platform"],
            webgl_vendor=StatsScraper.SLEATH_SETTINGS["webgl_vendor"],
            renderer=StatsScraper.SLEATH_SETTINGS["renderer"],
            fix_hairline=StatsScraper.SLEATH_SETTINGS["fix_hairline"],
        )
        self.page_load_time = page_load_time

    def get_stats(self, course_link: str):
        self.driver.get(course_link)
        sleep(self.page_load_time)
        soup = bs(self.driver.page_source, "html5lib")
        # Get stats
        id = self._get_id(soup)
        discount = self._get_discount(soup)
        discount_time_left = self._get_discount_time_left(soup)
        rating = self._get_rating(soup)
        students = self._get_students(soup)
        language = self._get_language(soup)
        badge = self._get_badge(soup)
        return {
            "id": id,
            "discount": discount,
            "discount_time_left": discount_time_left,
            "rating": rating,
            "students": students,
            "language": language,
            "badge": badge,
        }

    def _get_id(self, soup):
        id = soup.find("body", id="udemy")
        return id["data-clp-course-id"]

    def _get_discount(self, soup):
        discount = soup.find(
            "div",
            class_="price-text--price-part--2npPm ud-clp-percent-discount ud-text-sm",
        )
        discount_percentage = re.findall("[0-9]+", discount.text)[0]
        return int(discount_percentage)

    def _get_discount_time_left(self, soup):
        discount_time_left = soup.find(
            "span",
            {
                "data-purpose": "safely-set-inner-html:discount-expiration:expiration-text"
            },
        )
        return discount_time_left.text.split("left")[0]

    def _get_rating(self, soup):
        rating = soup.find("span", {"data-purpose": "rating-number"})
        return rating.text

    def _get_students(self, soup):
        students = soup.find("div", class_="enrollment")
        return students.text.split(" ")[0]

    def _get_language(self, soup):
        language = soup.find(
            "div",
            class_="clp-lead__element-item clp-lead__locale",
        )
        return language.text

    def _get_badge(self, soup):
        badge = soup.find(
            "div",
            class_=re.compile("udlite-badge udlite-heading-xs.*"),
        )
        if not badge:
            return None
        return badge.text
