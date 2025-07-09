from udemypy.udemy.scraper import DiscudemyScraper, YoFreeSamplesScraper, RealDiscountScraper, StatsScraper
from udemypy import course
from udemypy.udemy import settings
from udemypy import utils
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional
import time
import random
import asyncio
import time as pytime


def _delete_duplicated_courses(courses: List[dict]) -> List[dict]:
    return [dict(t) for t in {tuple(sorted(course.items())) for course in courses}]


def _scrape_courses(pages: int) -> List[course.Course]:
    """Return a list of courses without stats and id=None."""
    courses_scrapers = (
        DiscudemyScraper(pages),
        YoFreeSamplesScraper(pages),
        RealDiscountScraper(pages),
        # UdemyFreebiesScraper(pages),
    )
    
    # Track used coupon codes across all sources to avoid duplicates
    used_coupon_codes = set()
    scraped_courses = []
    
    for courses_scraper in courses_scrapers:
        courses_scraper.find_courses()
        
        # Filter out courses with duplicate coupon codes
        filtered_courses = []
        for course_data in courses_scraper.courses:
            coupon_code = course_data.get("coupon_code", "Unknown")
            if coupon_code != "Unknown" and coupon_code not in used_coupon_codes:
                used_coupon_codes.add(coupon_code)
                filtered_courses.append(course_data)
            else:
                # Update stats for skipped duplicate coupon
                courses_scraper.stats['skipped_duplicate_coupon'] = courses_scraper.stats.get('skipped_duplicate_coupon', 0) + 1
        
        scraped_courses.extend(filtered_courses)
    
    # Remove duplicates by link
    scraped_courses = _delete_duplicated_courses(scraped_courses)

    # Print global analytics
    _print_global_analytics(courses_scrapers, scraped_courses)
    
    # Save detailed reports
    final_courses = [
        course.Course(
            id=None,  # Let database auto-generate ID
            title=c["title"],
            link=c["link"],
            coupon_code=c["coupon_code"],
            date_found=c["date_found"],
        )
        for c in scraped_courses
    ]
    
    # Save comprehensive report
    utils.save_scraping_report(final_courses, courses_scrapers)
    utils.print_detailed_analytics(courses_scrapers, final_courses)

    return final_courses


def _print_global_analytics(scrapers, final_courses):
    """Print comprehensive analytics across all scrapers"""
    print("\n" + "="*80)
    print("🌐 GLOBAL SCRAPING ANALYTICS")
    print("="*80)
    
    total_found = sum(scraper.stats.get('total_found', 0) for scraper in scrapers)
    total_added = sum(scraper.stats.get('added', 0) for scraper in scrapers)
    total_errors = sum(scraper.stats.get('errors', 0) for scraper in scrapers)
    total_skipped_duplicate_coupon = sum(scraper.stats.get('skipped_duplicate_coupon', 0) for scraper in scrapers)
    
    print(f"📊 Total courses found across all sources: {total_found}")
    print(f"✅ Total courses added: {len(final_courses)}")
    print(f"❌ Total skipped (duplicate coupon codes): {total_skipped_duplicate_coupon}")
    print(f"⚠️  Total errors encountered: {total_errors}")
    
    if total_found > 0:
        global_success_rate = (len(final_courses) / total_found) * 100
        print(f"📈 Global success rate: {global_success_rate:.1f}%")
    
    print("\n📋 Breakdown by source:")
    for scraper in scrapers:
        scraper_name = scraper.__class__.__name__
        found = scraper.stats.get('total_found', 0)
        added = scraper.stats.get('added', 0)
        if found > 0:
            rate = (added / found) * 100
            print(f"  {scraper_name}: {added}/{found} ({rate:.1f}%)")
    
    print("="*80)


def _delete_shared_courses_dict(
    courses: List[course.Course], shared_courses: List[course.Course]
) -> List[course.Course]:
    shared_titles = {c.title for c in shared_courses}
    return [c for c in courses if c.title not in shared_titles]


def add_course_stats(course_: course.Course, stats_scraper=None) -> Optional[course.Course]:
    if stats_scraper is None:
        # Use dummy StatsScraper with no arguments, matching scraper.py
        stats_scraper = StatsScraper()
    try:
        start = pytime.time()
        stats = stats_scraper.get_stats(course_.link)
        course_id = stats.get("id")
        # Keep the original course ID if stats scraper returns "Unknown"
        if course_id == "Unknown":
            course_id = course_.id
        return course.Course(
            id=course_id,
            title=course_.title,
            link=course_.link,
            coupon_code=course_.coupon_code,
            date_found=course_.date_found,
            discount=stats.get("discount", 0),
            discount_time_left=stats.get("discount_time_left", "Unknown"),
            students=stats.get("students", "Unknown"),
            rating=stats.get("rating", "Unknown"),
            language=stats.get("language", "Unknown"),
            badge=stats.get("badge", "None"),
        )
    except asyncio.TimeoutError:
        print(f"[!] Timeout loading DiscUdemy page {course_.link}")
    except Exception as e:
        print(f"[!] Failed to load DiscUdemy page {course_.link}: {e}")
        return None


def add_courses_stats(
    courses: List[course.Course], max_workers: int = 2
) -> List[course.Course]:
    limit = 2  # adjust as needed
    limited_courses = courses[:limit]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        courses_with_stats = list(executor.map(add_course_stats, limited_courses))

    return [c for c in courses_with_stats if c is not None]


def new_courses(shared_courses: List[course.Course]) -> List[course.Course]:
    scraped_courses = _scrape_courses(settings.PAGES_TO_SCRAPE)
    return _delete_shared_courses_dict(scraped_courses, shared_courses)


def delete_non_free_courses(courses: List[course.Course]) -> List[course.Course]:
    # Since we're not adding stats, assume all DiscUdemy courses are free
    # (DiscUdemy typically only lists free courses)
    return courses


def delete_free_courses(courses: List[course.Course]) -> List[course.Course]:
    return [c for c in courses if c.discount is not None and c.discount < settings.FREE_COURSE_DISCOUNT]


def delete_old_courses(courses: List[course.Course], course_lifetime: int) -> List[course.Course]:
    from datetime import datetime

    filtered_courses = []
    for c in courses:
        try:
                        # Handle both string and datetime types for date_found
            if isinstance(c.date_found, str):
                start_date = datetime.strptime(c.date_found, "%Y-%m-%d %H:%M:%S")
            else:
                start_date = c.date_found
            delta = datetime.now() - start_date
            if delta.days < course_lifetime:
                filtered_courses.append(c)
        except Exception as e:
            print(f"[!] Error parsing date for course {c.title}: {e}")
    return filtered_courses
