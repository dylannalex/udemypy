from datetime import datetime

from udemypy.database import database
from udemypy.sender import SenderBot


def _get_courses(
    db: database.DataBase,
    social_media_name: str,
):
    courses = database.retrieve_courses(db)
    courses_shared = database.retrieve_courses_shared_to_social_media(
        db,
        social_media_name,
    )
    courses_shared_id = [c.id for c in courses_shared]
    new_courses = [c for c in courses if c.id not in courses_shared_id]
    return new_courses


def send_courses(
    db: database.DataBase,
    bot: SenderBot,
    social_media_name: str,
    social_media_id: int,
) -> None:
    # Get new courses
    new_courses = _get_courses(db, social_media_name)
    print(f"[-] {len(new_courses)} new courses to share!")
    if len(new_courses) == 0:
        return

    # Share new courses
    for course_ in new_courses:
        print(f"\n\n[BOT] Sending course: {course_.title}")
        try:
            bot.send_course(course_)
        except Exception as exception:
            print(
                f"Could not send course to {social_media_name}",
                f"Course Title: {course_.title}",
                f"Error: {exception}",
                sep="\n",
            )
            continue
        database.add_course_social_media(
            db,
            course_.id,
            social_media_id,
            datetime.now(),
        )
