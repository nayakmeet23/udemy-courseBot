import os
import json
import csv
from datetime import datetime

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def save_scraping_report(courses, scrapers, filename_prefix="scraping_report"):
    """Save a comprehensive scraping report in both CSV and JSON formats"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create reports directory if it doesn't exist
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    # Save courses data
    courses_data = []
    for course in courses:
        courses_data.append({
            'title': course.title,
            'link': course.link,
            'coupon_code': course.coupon_code,
            'date_found': str(course.date_found),
            'discount': course.discount,
            'rating': course.rating,
            'students': course.students,
            'language': course.language
        })
    
    # Collect all skipped courses from all scrapers
    all_skipped_courses = []
    for scraper in scrapers:
        if hasattr(scraper, 'skipped_courses'):
            all_skipped_courses.extend(scraper.skipped_courses)
    
    # Save JSON report
    json_filename = os.path.join(reports_dir, f"{filename_prefix}_{timestamp}.json")
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': timestamp,
            'summary': {
                'total_courses_found': len(courses),
                'scrapers_used': len(scrapers),
                'total_skipped_courses': len(all_skipped_courses)
            },
            'scraper_stats': {
                scraper.__class__.__name__: scraper.stats for scraper in scrapers
            },
            'courses': courses_data,
            'skipped_courses': all_skipped_courses
        }, f, indent=2, ensure_ascii=False)
    
    # Save CSV report for courses
    csv_filename = os.path.join(reports_dir, f"{filename_prefix}_{timestamp}.csv")
    if courses_data:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=courses_data[0].keys())
            writer.writeheader()
            writer.writerows(courses_data)
    
    # Save CSV report for skipped courses
    skipped_csv_filename = os.path.join(reports_dir, f"{filename_prefix}_skipped_{timestamp}.csv")
    if all_skipped_courses:
        with open(skipped_csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'website', 'reason'])
            writer.writeheader()
            writer.writerows(all_skipped_courses)
    
    print(f"\n📄 Reports saved:")
    print(f"  JSON: {json_filename}")
    print(f"  CSV (courses): {csv_filename}")
    if all_skipped_courses:
        print(f"  CSV (skipped): {skipped_csv_filename}")
    
    return json_filename, csv_filename, skipped_csv_filename if all_skipped_courses else None


def print_detailed_analytics(scrapers, final_courses):
    """Print detailed analytics with recommendations"""
    print("\n" + "="*80)
    print("🔍 DETAILED ANALYTICS & RECOMMENDATIONS")
    print("="*80)
    
    # Calculate totals
    total_found = sum(scraper.stats.get('total_found', 0) for scraper in scrapers)
    total_added = len(final_courses)
    total_errors = sum(scraper.stats.get('errors', 0) for scraper in scrapers)
    
    print(f"📊 OVERVIEW:")
    print(f"  • Total courses found: {total_found}")
    print(f"  • Total courses added: {total_added}")
    print(f"  • Total errors: {total_errors}")
    
    # ✅ Fix: Initialize success_rate variable
    success_rate = 0
    if total_found > 0:
        success_rate = (total_added / total_found) * 100
        print(f"  • Success rate: {success_rate:.1f}%")
    
    print(f"\n📋 SCRAPER PERFORMANCE:")
    for scraper in scrapers:
        scraper_name = scraper.__class__.__name__
        found = scraper.stats.get('total_found', 0)
        added = scraper.stats.get('added', 0)
        errors = scraper.stats.get('errors', 0)
        
        if found > 0:
            rate = (added / found) * 100
            print(f"  • {scraper_name}: {added}/{found} courses ({rate:.1f}%) - {errors} errors")
        else:
            print(f"  • {scraper_name}: No courses found - {errors} errors")
    
    print(f"\n💡 RECOMMENDATIONS:")
    if total_errors > 0:
        print(f"  ⚠️  {total_errors} errors detected - check network connectivity and site availability")
    
    if success_rate < 50 and total_found > 0:  # ✅ Fix: Add condition
        print(f"  ⚠️  Low success rate ({success_rate:.1f}%) - consider adjusting scraping parameters")
    
    if total_added == 0:
        print(f"  ⚠️  No new courses found - all courses may already be in database")
    
    print("="*80)
