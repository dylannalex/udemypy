from udemypy.udemy import scrapers
from udemypy.udemy.bot_settings import PAGES_TO_SCRAPE


def _scrape_courses(pages: int) -> list[dict]:
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


def _delete_duplicates(courses: list[dict]) -> list[dict]:
    return [dict(t) for t in {tuple(course.items()) for course in courses}]


def _add_course_stats(courses: list[dict]) -> list[dict]:
    courses_with_stats = []
    for course in courses:
        udemy_scraper = scrapers.UdemyScraper(course["link"])
        courses_with_stats.append(
            {
                **course,
                "rating": udemy_scraper.get_rating(),
                "students": udemy_scraper.get_students(),
            }
        )
    return courses_with_stats


def get_courses() -> list[dict]:
    new_courses = _delete_duplicates(_scrape_courses(PAGES_TO_SCRAPE))
    return _add_course_stats(new_courses)
