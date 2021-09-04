from udemypy.database.db_data import TABLE_NAME


def add_courses(db, courses) -> list:
    cursor = db.cursor()
    courses_added = []
    for course in courses:
        print(f'COURSE: {course["title"]}')
        try:
            cursor.execute(
                f"""INSERT INTO {TABLE_NAME} VALUES('{course['title']}', '{course['link']}', '{course['date']}');"""
            )
            print("SUCCESSFULLY ADDED\n")
            courses_added.append(course)

        except Exception as exception:
            print(f"FAILED - {exception}\n")

    db.commit()
    return courses_added


def retrieve_courses(cursor) -> list:
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    courses_added = []
    for row in cursor:
        courses_added.append(
            {"title": row[0], "link": row[1], "date": row[2].strftime("%Y-%m-%d")}
        )
    return courses_added


def remove_courses(db, courses) -> None:
    cursor = db.cursor()
    for course in courses:
        cursor.execute(f"""DELETE FROM {TABLE_NAME} WHERE title='{course['title']}';""")
    db.commit()
