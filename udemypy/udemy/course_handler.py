from udemypy.udemy import scraper
from udemypy import course
from udemypy.udemy import settings


def _delete_duplicated_courses(courses: list[dict]) -> list[dict]:
    return [dict(t) for t in {tuple(course.items()) for course in courses}]


def _scrape_courses(pages: int) -> list[course.Course]:
    """
    Returns a list of courses without stats and id=None.
    """
    # Scrape courses
    courses_scrapers = (
        scraper.DiscudemyScraper(pages),
        # scraper.UdemyFreebiesScraper(pages),
        # scraper.TutorialBarScraper(pages),
    )
    scraped_courses = []
    for courses_scraper in courses_scrapers:
        courses_scraper.find_courses()
        scraped_courses.extend(courses_scraper.courses)
    scraped_courses = _delete_duplicated_courses(scraped_courses)
    # Convert dict to Course instances
    courses = []
    for course_ in scraped_courses:
        courses.append(
            course.Course(
                id=None,
                title=course_["title"],
                link=course_["link"],
                coupon_code=course_["coupon_code"],
                date_found=course_["date_found"],
            )
        )
    return courses


def _delete_shared_courses_dict(
    courses: list[course.Course], shared_courses: list[course.Course]
) -> list[course.Course]:
    titles = [c.title for c in shared_courses]
    return [c for c in courses if c.title not in titles]


def add_courses_stats(courses: list[course.Course]) -> list[course.Course]:
    courses_with_stats = []
    for course_ in courses:
        stats_scraper = scraper.StatsScraper(
            settings.CHROMEDRIVER_PATH,
            settings.GOOGLE_CHROME_BIN,
            settings.PAGE_LOAD_TIME,
        )
        # stats_scrapper is inside the for loops so
        # the webdriver is refreshed on each course
        # link and prevent Udemy to hide course stats
        try:
            stats = stats_scraper.get_stats(course_.link_with_coupon)
        except Exception as exception:
            print(f"[ERROR] Error while adding courses stats: {exception}")

        # Create Course instance with its stats added
        courses_with_stats.append(
            course.Course(
                stats["id"],
                course_.title,
                course_.link,
                course_.coupon_code,
                course_.date_found,
                discount=stats["discount"],
                discount_time_left=stats["discount_time_left"],
                students=stats["students"],
                rating=stats["rating"],
                language=stats["language"],
                badge=stats["badge"],
            )
        )
    return courses_with_stats


def new_courses(shared_courses: list[course.Course]) -> list[dict]:
    """
    Find free Udemy courses, deletes already shared
    courses and returns them with their stats added.
    """
    scraped_courses = _scrape_courses(settings.PAGES_TO_SCRAPE)
    new_courses = _delete_shared_courses_dict(scraped_courses, shared_courses)
    new_courses_with_stats = add_courses_stats(new_courses)
    return new_courses_with_stats


def delete_non_free_courses(
    courses: list[course.Course],
) -> list[course.Course]:
    """
    Given a list of course.Course (with its stats), removes the courses
    that are not free (those which discount is below 100%)
    """
    return [c for c in courses if c.discount == settings.FREE_COURSE_DISCOUNT]


def delete_free_courses(
    courses: list[course.Course],
) -> list[course.Course]:
    """
    Given a list of course.Course (with its stats), removes the courses
    that are free (those which discount is 100%)
    """
    return [c for c in courses if c.discount < settings.FREE_COURSE_DISCOUNT]
