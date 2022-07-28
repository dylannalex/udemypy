from udemypy.udemy import scraper
from udemypy.udemy import course
from udemypy.udemy import settings


def _delete_duplicated_courses(courses: list[dict]) -> list[dict]:
    return [dict(t) for t in {tuple(course.items()) for course in courses}]


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
    return _delete_duplicated_courses(scraped_courses)


def _parse_courses(courses: list[dict]) -> list[course.Course]:
    parsed_courses = []
    for course_ in courses:
        parsed_courses.append(
            course.Course(
                int(course_["id"]),
                course_["title"],
                course_["link"],
                course_["coupon_code"],
                course_["date_found"],
            )
        )
    return parsed_courses


def _delete_shared_courses(
    courses: list[course.Course], shared_courses_id: list[int]
) -> list[course.Course]:
    return [c for c in courses if c.id not in shared_courses_id]


def new_courses(shared_courses_id: list[int]) -> list[dict]:
    """
    Find free Udemy courses, deletes already shared
    courses and returns them with their stats added.
    """
    scraped_courses = _parse_courses(_scrape_courses(settings.PAGES_TO_SCRAPE))
    return _delete_shared_courses(scraped_courses, shared_courses_id)


def add_courses_stats(courses: list[course.Course]) -> list[course.CourseWithStats]:
    courses_with_stats = []
    stats_scraper = scraper.StatsScraper(
        settings.CHROMEDRIVER_PATH,
        settings.GOOGLE_CHROME_BIN,
        settings.PAGE_LOAD_TIME,
    )
    # Find stats
    for course_ in courses:
        try:
            stats = stats_scraper.get_stats(course_.link_with_coupon)
        except AttributeError:
            continue

        # Create CourseWithStats instance
        courses_with_stats.append(
            course.CourseWithStats(
                course_.id,
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


def delete_non_free_courses(
    courses: list[course.CourseWithStats],
) -> list[course.CourseWithStats]:
    """
    Given a list of course.CourseWithStats, removes the courses
    that are not free (those which discount is below 100%)
    """
    return [c for c in courses if c.discount == settings.FREE_COURSE_DISCOUNT]
