import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from time import sleep
from udemypy.course import Course
from udemypy.sender.bot import SenderBot
from udemypy.sender.text import emojis


def _get_message(
    title, link, rating, students, language, discount_time_left, badge
) -> str:
    message = [
        f"_{title}_ {emojis.BOOKS}",
        " ",
        f"{emojis.STAR} {rating}/5",
        f"{emojis.PEOPLE_SILHOUETTE} {students} students",
        f"{emojis.GLOBE} {language.capitalize()}",
        f"{emojis.HOURGLASS} Free for {discount_time_left}",
        f"{emojis.LINK} {link}",
        " ",
        f"Follow me for more free Udemy courses {emojis.HEART}",
    ]

    # Add course badge (if any)
    _badge_index = 2
    if badge:
        message.insert(_badge_index, f"{emojis.TROPHY} {badge}")

    return "\n".join(message)


class WhatsAppBot(SenderBot):
    text_box_class_name = "_3Uu1_"
    time_after_writing = 10
    time_between_message = 2

    def __init__(self, chromedriver_path: str):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("log-level=3")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        self.driver = webdriver.Chrome(
            options=options, executable_path=chromedriver_path
        )

    def connect(self) -> None:
        print("[BOT] Loading WhatsApp...")
        self.driver.get("https://web.whatsapp.com/")
        print("[BOT] Scan the QR code and sel3ect a chat to send courses")
        input("\nPress Enter when ready...")

    def send_course(self, course: Course) -> None:
        # Get message
        message = _get_message(
            course.title,
            course.link_with_coupon,
            course.rating,
            course.students,
            course.language,
            course.discount_time_left,
            course.badge,
        )
        pyperclip.copy(message)

        # Send message
        act = ActionChains(self.driver)
        text_box = self.driver.find_element(
            By.CLASS_NAME, __class__.text_box_class_name
        )
        text_box.click()
        act.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
        sleep(__class__.time_after_writing)
        text_box.send_keys(Keys.RETURN)
        sleep(__class__.time_between_message)
