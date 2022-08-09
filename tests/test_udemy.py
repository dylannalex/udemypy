from tests import _logs
from udemypy.udemy import course_handler
from udemypy import course


@_logs.test_function
def test_scrapers():
    courses: list[course.Course] = course_handler.new_courses([])
    for c in courses:
        print(f"{c.title}: {c.link}")
    return courses


@_logs.test_function
def test_add_courses_stats(course_: course.Course):
    """
    Tests add_courses_stats with only one course (to fast the
    execution)
    """
    course_with_stats: course.CourseWithStats
    course_with_stats = course_handler.add_courses_stats([course_])[0]
    print(
        f"""
title: {course_with_stats.title}
link: {course_with_stats.link_with_coupon}
discount: {course_with_stats.discount}
discount_time_left: {course_with_stats.discount_time_left}
students: {course_with_stats.students}
rating: {course_with_stats.rating}
language: {course_with_stats.language}
badge: {course_with_stats.badge}
\n\n"""
    )


def test_udemy():
    courses = test_scrapers()
    test_add_courses_stats(courses[0])


if __name__ == "__main__":
    test_udemy()
