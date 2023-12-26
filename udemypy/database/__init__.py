from udemypy.database.database import DataBase


def __get_commit_confirmation():
    while True:
        commit = input("[-] Commit? (y/n): ")
        if commit == "y":
            return True
        if commit == "n":
            return False


def debug(db: DataBase):
    print("[Database Debug]")
    commit = __get_commit_confirmation()
    while True:
        query = input("$ ")
        if query == "exit":
            return
        try:
            output = db.execute(query, commit)
        except Exception as exception:
            print(f"[-] ERROR: {exception}")

        if output is not None:
            print(output)
