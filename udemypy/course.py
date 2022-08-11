from datetime import datetime


class Course:
    def __init__(
        self,
        id: int,
        title: str,
        link: str,
        coupon_code: str,
        date_found: datetime,
        discount: int = None,
        discount_time_left: str = None,
        students: str = None,
        rating: str = None,
        language: str = None,
        badge: str or None = None,
    ):
        """
        Arguments:
            @id: course id
            @title: course title
            @link: course link
            @coupon_code: course discount coupon code
            @date_found: date when the course was scraped
            @discount: discount percentage (1 to 100)
            @discount_time_left: discount time left (hours or days)
            @students: number of students enrolled to the course
            @rating: course rating (from 0 to 5). It's a str value since it needs to be precise
            @language: course language
            @badge: course badge (Bestseller, Highest rated, etc)
        """
        self.id = id
        self.title = title
        self.link = link
        self.coupon_code = coupon_code
        self.date_found = date_found
        self.discount = discount
        self.discount_time_left = discount_time_left
        self.students = students
        self.rating = rating
        self.language = language
        self.badge = badge

    @property
    def link_with_coupon(self):
        return f"{self.link}?couponCode={self.coupon_code}"
