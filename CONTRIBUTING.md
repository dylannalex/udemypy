<p align="center">
  <img width="350" height="350" src="../media/contributing-logo.png?raw=true">
</p>

Thank you for your interest in contributing to UdemyPy:heart:

This guide starts with a general description of the different ways to contribute
to UdemyPy, then we explain some technical aspects of preparing your contribution.

## What are the different ways to contribute?

### Spread the Word

The best way you can contribute, is to share your enthusiasm about UdemyPy with
other people. Talk about UdemyPy with your family and friends, and help this
learning lovers community continue growing!

### Report a bug

If you have a bug report just open an issue! Go to
<https://github.com/dylannalex/udemypy/issues>. It's possible that your issue was
already addressed. If it wasn't, open it.

### UdemyPy development

All development-related contributions are accepted, such as documentation
improvement, adding features, bug fixing, etc. Please read the following sections
to learn more about the technical aspects of UdemyPy.

## UdemyPy structure

In order to contribute to UdemyPy development, it helps to understand the structure
of the code. UdemyPy is structured in
[packages](https://docs.python.org/3/tutorial/modules.html#packages). Each package
has a specific functionality. In this section you can find a description of each
package and its modules.

### [udemypy.udemy](./udemypy/udemy) package

This package is responsible for Udemy courses scraping.

- `scraper.py`: contains `_CoursesScraper` classes, which scrapes free Udemy
  courses link from Discudemy, Udemy Freebies and Tutorial Bar; and a
  `StatsScraper` class, that scrapes courses stats from Udemy website.
- `course_handler.py`: handles `scraper.py` scrapers.
- `settings.py`: contains environment variables and constants used in this package.

### [udemypy.database](./udemypy/database) package

This package is responsible for database management.

- `database.py`: enables database access (adding, reading and removing courses).
- `script.py`: reads and interprets sql scripts.
- `setup.py`: setups database tables.
- `settings.py`: contains environment variables and constants used in this package.

### [udemypy.text](./udemypy/text) package

This package handles text validation and styling.

- `emojis.py`: contains a list of emojis (unicode value).
- `markdown_validation.py`: prepares text for Markdown parser.


### [udemypy.tgm](./udemypy/tgm) package

This package is responsible for sharing courses to Telegram.

- `message.py`: generates messages to share to Telegram channel.
- `tgm_bot.py`: handles Telegram bot.
- `settings.py`: contains environment variables and constants used in this package.

### [udemypy.twitter](./udemypy/twitter) package

This package is responsible for sharing courses to Twitter.

- `message.py`: generates messages to share to Twitter.
- `twitter_bot.py`: handles Twitter bot.
- `settings.py`: contains environment variables and constants used in this package.

## How UdemyPy works

To find, share and keep track of free Udemy courses, UdemyPy has three main
processes.

### Finding courses

UdemyPy scrapes free Udemy courses, retrieves courses from the database and save
the new free courses found.

You can start this process with the command:

```bash
python -m udemypy.find_courses
```

### Removing courses

UdemyPy retrieves the Udemy courses from the database and checks if they are
still free. Courses that are no longer free are removed from the database.

You can start this process with the command:

```bash
python -m udemypy.clean_database
```

### Sharing courses

UdemyPy retrieves from the database the Udemy courses that haven't been shared
to social media and posts them to Twitter and Telegram.

You can start this process with the command:

```bash
python -m udemypy.send_courses
```

**Note:** the order in which this processes are executed is crucial. You have
to find the courses before sharing them, and if you share courses before cleaning
the database you take the risk of sharing non-free courses.

## Setup a Development Environment

### Fork and Clone UdemyPy

First, you'll need to *get* our project. This is the appropriate *clone* command (if
you're unfamiliar with this process, <https://help.github.com/articles/fork-a-repo>):

**DO THIS (in the directory where you want the repo to live)**

```bash
git clone https://github.com/your_github_username/udemypy.git
cd udemypy
```

**Note:** if you're just getting started with git, there exist great resources to
learn and become confident about git, like <http://try.github.io/>.

### Set up a virtual environment

You can use either conda or virtualenv to create a virtual environment for
UdemyPy development, e.g.

```bash
python -m venv udemypy-venv
source udemypy-venv/Scripts/activate
```

After creating a virtual environment, install requirements.

```bash
(udemypy-venv) $ pip install -r requirements.txt
```

## Environment variables

Environment variables are grouped by package, located at the `settings.py` module.
In this section you can find a brief description for each environment variable.

[udemypy.udemy](./udemypy/udemy/settings.py) environment variables:

- `PAGE_LOAD_TIME`: sleep time to wait for a website to load (**int**).
- `PAGES_TO_SCRAPE`: number of pages to scrape from Discudemy, UdemyFreebies
  and TutorialBar (**int**).
- `CHROMEDRIVER_PATH`: path to [chrome-webdriver](https://chromedriver.chromium.org/)
  (**str**).
- `GOOGLE_CHROME_BIN`: Google Chrome bin path (needed for
  [Heroku Deployment](#heroku-deployment)) (**str**).

[udemypy.database](./udemypy/database/settings.py) environment variables:

- `DATABASE_URL`: database connection URL (**str**).

[udemypy.tgm](./udemypy/tgm/settings.py) environment variables:

- `TOKEN`: Telegram API token (**str**).
- `CHANNEL_ID`: Telegram channel ID. Free courses will be shared in this channel (bot
  must be admin of this channel in order to send messages) (**str**).
- `CHANNEL_LINK`: link shown when the 'share channel' button on the free course message
  is clicked (**str**).
- `TWITTER_LINK`: link shown when the 'twitter' button on the free course message is
  clicked (**str**).

[udemypy.twitter](./udemypy/twitter/settings.py) environment variables:

- `API_KEY`: Twitter API key (**str**).
- `API_KEY_SECRET`: Twitter secret API key (**str**).
- `ACCESS_TOKEN`: Twitter access token (**str**).
- `ACCESS_TOKEN_SECRET`: Twitter secret access token (**str**).

**Note:** you only need to set the environment variables from the package you are using, e.g.,
if you are running `python -m udemypy.find_courses` you only need to set
[udemypy.database](./udemypy/database/settings.py) and
[udemypy.udemy](./udemypy/udemy/settings.py) environment variables.


