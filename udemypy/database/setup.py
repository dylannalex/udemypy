from udemypy.database import database
from udemypy.database import script


def setup_database():
    db: database.DataBase = database.connect()
    db.execute_script(
        script.read_script(script.get_path("create_tables.sql")),
        commit=True,
    )
    db.execute_script(
        script.read_script(script.get_path("setup_tables.sql")),
        commit=True,
    )


if __name__ == "__main__":
    setup_database()
