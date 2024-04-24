from udemypy.udemy import scraper
from udemypy import course
from udemypy.udemy import settings
from concurrent.futures import ThreadPoolExecutor


def _delete_duplicated_courses(courses: list[dict]) -> list[dict]:
    return [dict(t) for t in {tuple(course.items()) for course in courses}]


def _scrape_courses(pages: int) -> list[course.Course]:
    """
    Returns a list of courses without stats and id=None.
    """
    # Scrape courses
    courses_scrapers = (
        scraper.DiscudemyScraper(pages),
        scraper.UdemyFreebiesScraper(pages),
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


def add_course_stats(
    course_: course.Course,
    stats_scraper: scraper.StatsScraper = None,
) -> course.Course:
    """Adds stats to a single course."""
    if stats_scraper is None:
        stats_scraper = scraper.StatsScraper(
            settings.CHROMEDRIVER_PATH,
            settings.GOOGLE_CHROME_BIN,
            settings.PAGE_LOAD_TIME,
        )
    try:
        stats = stats_scraper.get_stats(course_.link_with_coupon)
        return course.Course(
            id=stats["id"],
            title=course_.title,
            link=course_.link,
            coupon_code=course_.coupon_code,
            date_found=course_.date_found,
            discount=stats["discount"],
            discount_time_left=stats["discount_time_left"],
            students=stats["students"],
            rating=stats["rating"],
            language=stats["language"],
            badge=stats["badge"],
        )
    except Exception as exception:
        print(f"[ERROR] Error while adding courses stats: {exception}")


def add_courses_stats(
    courses: list[course.Course],
    max_workers: int = 5,
) -> list[course.Course]:
    """Adds stats to a list of courses concurrently."""
    with ThreadPoolExecutor(max_workers) as executor:
        courses_with_stats = list(executor.map(add_course_stats, courses))
    return [c for c in courses_with_stats if c is not None]


def new_courses(shared_courses: list[course.Course]) -> list[dict]:
    """
    Find free Udemy courses, deletes already shared
    courses and returns them without their stats added.

    Note: the new courses found have id=None, as id is
    scraped by StatsScraper.
    """
    scraped_courses = _scrape_courses(settings.PAGES_TO_SCRAPE)
    new_courses = _delete_shared_courses_dict(scraped_courses, shared_courses)
    return new_courses


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


def delete_old_courses(
    courses: list[course.Course], course_lifetime: int
) -> list[course.Course]:
    """
    Given a list of course.Course, removes the courses that have
    been store longer than the course lifetime.
    """
    from datetime import datetime

    courses_to_delete = []
    for c in courses:
        start_date = datetime.strptime(c.date_found, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.now()
        delta = end_date - start_date
        if delta.days >= course_lifetime:
            courses_to_delete.append(c)

    return courses_to_delete
