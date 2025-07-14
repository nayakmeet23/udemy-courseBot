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
        current_price: Optional[str] = None,
        previous_price: Optional[str] = None,
        rating: Optional[str] = None,
        category: Optional[str] = None,
        image_url: Optional[str] = None,
        students: Optional[str] = None,
        language: Optional[str] = None,
        badge: Optional[str] = None,
        discount_time_left: Optional[str] = None,
        source: Optional[str] = None,
    ):
        """
        Arguments:
            @id: course id
            @title: course title
            @link: course link
            @coupon_code: course discount coupon code
            @date_found: date when the course was scraped
            @current_price: current price of the course
            @previous_price: previous price of the course
            @rating: course rating (as string)
            @category: course category
            @image_url: course image url
            @students: number of students enrolled to the course
            @language: course language
            @badge: course badge (Bestseller, Highest rated, etc)
            @discount_time_left: discount time left (hours or days)
            @source: source website name
        """
        self.id = id
        self.title = title
        self.link = link
        self.coupon_code = coupon_code
        self.date_found = date_found
        self.current_price = current_price
        self.previous_price = previous_price
        self.rating = rating
        self.category = category
        self.image_url = image_url
        self.students = students
        self.language = language
        self.badge = badge
        self.discount_time_left = discount_time_left
        self.source = source

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
