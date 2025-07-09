from udemypy import course
from udemypy.udemy import course_handler
from udemypy.udemy import settings as udy_setts
from udemypy.database import database


def _save_courses(db, courses: list[course.Course]):
    from udemypy.database import database as dbmod
    for course_ in courses:
        try:
            if dbmod.course_exists_by_link(db, course_.link):
                print(f'Course "{course_.title}" already exists in the database (by link)')
                continue
            database.add_course(
                db,
                course_.id,  # This will be None, letting DB auto-increment
                course_.title,
                course_.link,  # This now contains the full link with coupon code
                course_.coupon_code,
                str(course_.date_found) if course_.date_found else "",
                100,  # Assume all courses are free (100% discount)
                "Unknown",  # discount_time_left
                "Unknown",  # students
                "Unknown",  # rating
                "Unknown",  # language
                "Unknown",  # badge
            )
        except Exception as exception:
            # Handle duplicate entry errors gracefully
            if "Duplicate entry" in str(exception) and "for key 'title'" in str(exception):
                # Course already exists, skip silently
                continue
            else:
                # Other errors should still be reported
                print(
                    f"[Database] Could not save course {course_.title}\nERROR: {exception}"
                )


def find_courses(db: database.DataBase, verbose: bool):
    # Retrieve shared courses
    courses_on_database = database.retrieve_courses(db)

    if verbose:
        print(f"[-] {len(courses_on_database)} courses on database")

    # Find new free courses with their stats
    new_courses = course_handler.new_courses(courses_on_database)

    if verbose:
        print(f"[-] {len(new_courses)} new courses found")

        # Check if new courses found don't exceed the max courses to send
        # limit
        if len(new_courses) > udy_setts.MAX_COURSES_TO_SEND:
            print(
                f"[-] Total courses found exceed the limit of {udy_setts.MAX_COURSES_TO_SEND}",
            )
            print(
                f"[-] Removing {len(new_courses) - udy_setts.MAX_COURSES_TO_SEND} courses from `new_courses` list",
            )
            new_courses = new_courses[0 : udy_setts.MAX_COURSES_TO_SEND]

    # Skip stats processing entirely - use courses directly
    free_courses = course_handler.delete_non_free_courses(new_courses)
    if verbose:
        print(f"[-] {len(free_courses)} free courses found")

    # Add courses to database
    _save_courses(db, free_courses)


if __name__ == "__main__":
    db = database.connect()
    find_courses(db, verbose=True)
