from datetime import datetime
from typing import Union, Optional


class Course:
    def __init__(
        self,
        id: Optional[int],
        title: str,
        link: str,
        coupon_code: str,
        date_found: Union[datetime, str],
        discount: Optional[int] = None,
        discount_time_left: Optional[str] = None,
        students: Optional[str] = None,
        rating: Optional[str] = None,
        language: Optional[str] = None,
        badge: Optional[str] = None,
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
        """Return the course link with coupon code, avoiding duplicates"""
        # Check if the link already contains a coupon code
        if "couponCode=" in self.link:
            # If coupon code is already in the link, return the link as is
            return self.link
        else:
            # If no coupon code in link, append it
            return f"{self.link}?couponCode={self.coupon_code}"
