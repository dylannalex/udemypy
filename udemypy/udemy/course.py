from datetime import datetime


class Course:
    def __init__(
        self, id: int, title: str, link: str, coupon_code: str, date_found: datetime
    ):
        """
        Attributes:
            @id: course id
            @title: course title
            @link: course link
            @coupon_code: course discount coupon code
            @date_found: date when the course was scraped
            @full_link: link containing coupon code
        """
        self.id = id
        self.title = title
        self.link = link
        self.coupon_code = coupon_code
        self.date_found = date_found

    @property
    def full_link(self):
        return f"{self.link}?couponCode={self.coupon_code}"


class CourseWithStats(Course):
    def __init__(
        self,
        id: int,
        title: str,
        link: str,
        coupon_code: str,
        date_found: datetime,
        students: str,
        rating: str,
    ):
        """
        Attributes:
            @students: number of students enrolled to the course
            @rating: course rating (from 0 to 5). It's a str value since it needs to be precise
        """
        super().__init__(id, title, link, coupon_code, date_found)
        self.students = students
        self.rating = rating
