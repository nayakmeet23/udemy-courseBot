from os import getenv

MAX_COURSES_TO_SEND = int(getenv("MAX_COURSES_TO_SEND", 100))
PAGES_TO_SCRAPE = int(getenv("PAGES_TO_SCRAPE", 2))
CHROMEDRIVER_PATH = getenv("CHROMEDRIVER_PATH")
GOOGLE_CHROME_BIN = getenv("GOOGLE_CHROME_BIN")
PAGE_LOAD_TIME = getenv("PAGE_LOAD_TIME")
PAGE_LOAD_TIME = None if PAGE_LOAD_TIME is None else int(PAGE_LOAD_TIME)

FREE_COURSE_DISCOUNT = 100
# This will be used in course_handler.py
MAX_COURSES = MAX_COURSES_TO_SEND

# Fast mode settings for maximum speed
FAST_MODE = getenv("FAST_MODE", "true").lower() == "false"  # Enable fast mode by default
MAX_COURSES_TO_PROCESS = int(getenv("MAX_COURSES_TO_PROCESS", 10))  # Process only 10 courses in fast mode