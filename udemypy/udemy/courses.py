from udemypy.udemy import scraper
from udemypy.udemy.settings import PAGES_TO_SCRAPE


def _scrape_courses(pages: int) -> list[dict]:
    courses_scrapers = (
        scraper.DiscudemyScraper(pages),
        scraper.UdemyFreebiesScraper(pages),
        scraper.TutorialBarScraper(pages),
    )
    scraped_courses = []
    for courses_scraper in courses_scrapers:
        courses_scraper.find_courses()
        scraped_courses.extend(courses_scraper.courses)

    return scraped_courses


def _delete_duplicates(courses: list[dict]) -> list[dict]:
    return [dict(t) for t in {tuple(course.items()) for course in courses}]


def _add_course_stats(courses: list[dict]) -> list[dict]:
    courses_with_stats = []
    for course in courses:
        stats_scraper = scraper.StatsScraper(course["link"])
        courses_with_stats.append(
            {
                **course,
                "rating": stats_scraper.get_rating(),
                "students": stats_scraper.get_students(),
            }
        )
    return courses_with_stats


def get_courses() -> list[dict]:
    new_courses = _delete_duplicates(_scrape_courses(PAGES_TO_SCRAPE))
    return _add_course_stats(new_courses)
