# UdemyPy :robot:	

<p align="center">
  <img width="200" height="200" src="../media/udemypy-logo.png?raw=true">
</p>

**UdemyPy** is a bot that hourly searches for Udemy free courses and shares them on:
- [Telegram](https://t.me/freecourses000)
- [Twitter](https://twitter.com/UdemyPy)


## :electric_plug: How does it work?

For publishing new courses, UdemyPy follows these steps:

1. UdemyPy looks for courses at Discudemy, UdemyFreebies and TutorialBar.
2. The courses found are compared to those previously found. A `new_courses` list is generated and stored into the database.
3. `new_courses` are shared on social media.

This process is run hourly, everyday.

## :electric_plug: How are repeated courses detected?

Since UdemyPy scrapes different websites constantly, it must remember which courses have already been shared.<br/>
Every hour UdemyPy gets a list of free Udemy courses: `courses_found`. This list contains courses which haven't been shared
yet and courses that have. For each course in `courses_found`, UdemyPy tries to add it to the database. If it fails, the course
is already in the database (therefore the course has already been shared). If it success, the course is stored in a `courses_added`
list.<br/>
Finally, the `courses_added` list is shared on social media.

## :electric_plug: Enviroment Variables

#### FILE: udemypy/udemy/settings.py

```
PAGES_TO_SCRAPE: number of pages to scrape from Discudemy, UdemyFreebies and TutorialBar.
```
#### FILE: udemypy/database/settings.py

```
CLEARDB_DATABASE_URL: url provided by Heroku ClearDB.
COURSE_LIFETIME: days a course will be stored in the database.
TABLE_NAME: name of the table where courses are stored.
```

#### FILE: udemypy/tgm/settings.py

```
TOKEN: token to establish connection with the Telegram API.
CHANNEL_ID: Telegram channel id (could be a number or string).
CHANNEL_LINK: link shown when you click the share button from a Telegram message sent by UdemyPy.
DONATE_ME_LINK: link shown when you click the donate button from a Telegram message sent by UdemyPy.
TWITTER_LINK: link shown when you click the twitter button from a Telegram message sent by UdemyPy.
```

#### FILE: udemypy/twitter/settings.py

```
API_KEY: key provided by Twitter to use its API.
API_KEY_SECRET: key provided by Twitter to use its API.
ACCESS_TOKEN: token provided by Twitter to use its API.
ACCESS_TOKEN_SECRET: token provided by Twitter to use its API.
```
