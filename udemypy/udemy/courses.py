from udemypy.udemy import scrapers
from udemypy.udemy.bot_settings import PAGES_TO_SCRAPE


def __scrape_courses(pages: int) -> list:
    courses_scrapers = (
        scrapers.DiscudemyScraper(pages),
        scrapers.UdemyFreebiesScraper(pages),
        scrapers.TutorialBarScraper(pages),
    )
    scraped_courses = []
    for scraper in courses_scrapers:
        scraper.find_courses()
        scraped_courses.extend(scraper.courses)

    return scraped_courses


def __delete_duplicates(courses: list) -> list:
    return [dict(t) for t in {tuple(course.items()) for course in courses}]


def get_courses() -> list:
    return __delete_duplicates(__scrape_courses(PAGES_TO_SCRAPE))
