from datetime import datetime
from udemypy.database.connection import DataBase
from udemypy.database import connection
from udemypy.database import settings
from udemypy.database import script
from udemypy import course
from typing import Optional


def connect() -> DataBase:
    database = settings.DATABASE
    if database == "mysql":
        try:
            db = connection.MySqlDataBase(settings.DATABASE_URL)
        except ImportError:
            print("[ERROR] MySQL connector not available. Install mysql-connector-python")
            raise ImportError("MySQL connector not available. Install mysql-connector-python")
    elif database == "sqlite3":
        print("[ERROR] SQLite is not supported. Use MySQL only.")
        raise ValueError("SQLite is not supported. Use MySQL only.")
    else:
        print("[ERROR] Only MySQL is supported. Set DATABASE=mysql")
        raise ValueError("Only MySQL is supported. Set DATABASE=mysql")
    return db


def add_course(
    db: DataBase,
    course_id: Optional[int],
    course_title: str,
    course_link: str,
    course_coupon: str,
    date_found: str,
    discount: Optional[int],
    discount_time_left: Optional[str],
    students: Optional[str],
    rating: Optional[str],
    language: Optional[str],
    badge: Optional[str],
) -> None:
    """Adds a course instance to the database."""
    script_path = script.get_path("add_course.sql")
    variables = {
        "title_value": course_title,
        "link_value": course_link,
        "coupon_code_value": course_coupon,
        "date_found_value": date_found,
        "discount_value": discount,
        "discount_time_left_value": discount_time_left,
        "students_value": students,
        "rating_value": rating,
        "lang_value": language,
        "badge_value": badge,
    }
    sql_script = script.read_script(script_path, variables)
    db.execute_script(sql_script, commit=True)


def add_course_social_media(
    db: DataBase,
    course_id: int,
    social_media_id: int,
    date_time_shared: datetime,
):
    """Adds a course_social_media instance to the database."""
    script_path = script.get_path("add_course_social_media.sql")
    variables = {
        "course_id_value": course_id,
        "social_media_id_value": social_media_id,
        "date_time_shared_value": date_time_shared,
    }
    sql_script = script.read_script(script_path, variables)
    db.execute_script(sql_script, commit=True)


def retrieve_courses(db: DataBase) -> list[course.Course]:
    """Retrieves all courses from database."""
    script_path = script.get_path("retrieve_courses.sql")
    sql_script = script.read_script(script_path)
    courses = []
    for course_values in db.execute_script(sql_script, commit=False):
        courses.append(course.Course(*course_values))
    return courses


def retrieve_courses_shared_to_social_media(
    db: DataBase,
    social_media_name: str,
) -> list[course.Course]:
    """Retrieves courses that have been shared to a given social media."""
    script_path = script.get_path("retrieve_courses_shared.sql")
    variables = {"social_media_name_value": social_media_name}
    sql_script = script.read_script(script_path, variables)
    courses = []
    for course_values in db.execute_script(sql_script, commit=False):
        courses.append(course.Course(*course_values))
    return courses


def retrieve_courses_shared_to_twitter(db: DataBase) -> list[course.Course]:
    """Retrieves courses that have been shared to Twitter."""
    script_path = script.get_path("retrieve_courses_shared_to_twitter.sql")
    sql_script = script.read_script(script_path)
    courses = []
    for course_values in db.execute_script(sql_script, commit=False):
        courses.append(course.Course(*course_values))
    return courses


def retrieve_courses_shared_to_telegram(db: DataBase) -> list[course.Course]:
    """Retrieves courses that have been shared to Telegram."""
    script_path = script.get_path("retrieve_courses_shared_to_telegram.sql")
    sql_script = script.read_script(script_path)
    courses = []
    for course_values in db.execute_script(sql_script, commit=False):
        courses.append(course.Course(*course_values))
    return courses


def remove_course(db: DataBase, course_id: int) -> None:
    """
    Removes a course instance with their course_social_media instances
    from database.
    """
    script_path = script.get_path("remove_course.sql")
    variables = {"id_value": course_id}
    sql_script = script.read_script(script_path, variables)
    db.execute_script(sql_script, commit=True)


def course_exists_by_link(db: DataBase, course_link: str) -> bool:
    """Check if a course with the given link already exists in the database."""
    query = f"SELECT COUNT(*) FROM course WHERE link = '{course_link}'"
    result = db.execute(query, commit=False)
    return result[0][0] > 0 if result else False
