import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from typing import List
import json
import re
from urllib.parse import urljoin, urlparse
import random

from udemypy import course
from udemypy.udemy import settings


class _CoursesScraper(ABC):
    HEADERS_LIST = [
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
        {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
    ]

    def __init__(self):
        self.courses = []
        self.stats = {
            "total_found": 0,
            "added": 0,
            "skipped_duplicate_coupon": 0,
            "skipped_no_coupon": 0,
            "errors": 0,
        }

    def get_random_headers(self):
        return random.choice(self.HEADERS_LIST)

    @abstractmethod
    def find_courses(self) -> None:
        pass

    def _add_course(self, title, link):
        # Extract coupon code from link
        coupon_code = ""
        if "couponCode=" in link:
            coupon_code = link.split("couponCode=")[1].split("&")[0]
        elif "coupon=" in link:
            coupon_code = link.split("coupon=")[1].split("&")[0]
        elif "discount=" in link:
            coupon_code = link.split("discount=")[1].split("&")[0]

        # Skip if no coupon code found
        if not coupon_code:
            self.stats["skipped_no_coupon"] += 1
            return

        # Check for duplicate by (title, link, coupon_code)
        existing_keys = {(c.title, c.link, c.coupon_code) for c in self.courses}
        if (title, link, coupon_code) in existing_keys:
            self.stats["skipped_duplicate_coupon"] += 1
            return

        # Create course object
        course_obj = course.Course(
            id=None,
            title=title,
            link=link,
            coupon_code=coupon_code,
            date_found=time.strftime("%Y-%m-%d %H:%M:%S"),
        )

        self.courses.append(course_obj)
        self.stats["added"] += 1
        self.stats["total_found"] += 1

    def print_analytics(self, scraper_name):
        print(f"\n📊 {scraper_name} Analytics:")
        print(f"   Total found: {self.stats['total_found']}")
        print(f"   Added: {self.stats['added']}")
        print(f"   Skipped (no coupon): {self.stats['skipped_no_coupon']}")
        print(f"   Skipped (duplicate): {self.stats['skipped_duplicate_coupon']}")
        print(f"   Errors: {self.stats['errors']}")


class DiscudemyScraper(_CoursesScraper):
    def __init__(self, pages):
        super().__init__()
        self.pages = pages
        self.base_url = "https://www.discudemy.com/all/"

    async def _make_request_with_retry(self, session, url, page_num):
        max_retries = 3
        retry_delays = [2, 5, 10]

        for attempt in range(max_retries + 1):
            try:
                headers = self.get_random_headers()
                async with session.get(url, headers=headers, timeout=30) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        print(f"[DiscUdemy] Page {page_num} returned status {response.status}")
                        return None
            except Exception as e:
                if attempt < max_retries:
                    delay = retry_delays[attempt]
                    print(f"[DiscUdemy] Attempt {attempt + 1} failed for page {page_num}, retrying in {delay}s: {e}")
                    await asyncio.sleep(delay)
                else:
                    print(f"[DiscUdemy] Failed to fetch page {page_num} after {max_retries} attempts: {e}")
                    self.stats["errors"] += 1
                    return None

    async def _fetch_all_course_links(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for page in range(1, self.pages + 1):
                url = f"{self.base_url}{page}"
                task = self._make_request_with_retry(session, url, page)
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            return responses

    def find_courses(self):
        print(f"[DiscUdemy] Scraping {self.pages} pages...")
        
        # Run async scraping
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            responses = loop.run_until_complete(self._fetch_all_course_links())
            loop.run_until_complete(self._scrape_course_details(responses))
        finally:
            loop.close()

    async def _scrape_course_details(self, responses):
        async with aiohttp.ClientSession() as session:
            for page_num, response in enumerate(responses, 1):
                if not response or isinstance(response, Exception):
                    continue

                try:
                    # Use html5lib parser instead of lxml
                    soup = BeautifulSoup(response, 'html5lib')
                    
                    # Find course cards
                    course_cards = soup.find_all('div', class_='card')
                    
                    for card in course_cards:
                        try:
                            # Extract course link
                            link_elem = card.find('a', href=True)
                            if not link_elem:
                                continue
                            
                            course_url = link_elem['href']
                            if not course_url.startswith('http'):
                                course_url = urljoin(self.base_url, course_url)
                            
                            # Extract title
                            title_elem = card.find('h3') or card.find('h2') or card.find('h1')
                            if not title_elem:
                                continue
                            
                            title = title_elem.get_text(strip=True)
                            
                            # Follow redirect to get Udemy link
                            async def process_course(course_url):
                                try:
                                    headers = self.get_random_headers()
                                    async with session.get(course_url, headers=headers, timeout=30, allow_redirects=True) as resp:
                                        if resp.status == 200:
                                            final_url = str(resp.url)
                                            if 'udemy.com' in final_url:
                                                self._add_course(title, final_url)
                                                self.stats["total_found"] += 1
                                except Exception as e:
                                    print(f"[DiscUdemy] Error processing course {course_url}: {e}")
                                    self.stats["errors"] += 1
                            
                            await process_course(course_url)
                            
                        except Exception as e:
                            print(f"[DiscUdemy] Error parsing course card: {e}")
                            self.stats["errors"] += 1
                            
                except Exception as e:
                    print(f"[DiscUdemy] Error parsing page {page_num}: {e}")
                    self.stats["errors"] += 1


class YoFreeSamplesScraper(_CoursesScraper):
    def __init__(self, pages):
        super().__init__()
        self.pages = pages
        self.base_url = "https://yofreesamples.com/courses/free-discounted-udemy-courses-list/"

    def find_courses(self):
        print(f"[YoFreeSamples] Scraping {self.pages} pages...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self._scrape_courses())
        finally:
            loop.close()

    async def _make_request_with_retry(self, session, url):
        max_retries = 3
        retry_delays = [2, 5, 10]
        for attempt in range(max_retries + 1):
            try:
                headers = self.get_random_headers()
                async with session.get(url, headers=headers, timeout=30) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        print(f"[YoFreeSamples] Returned status {response.status}")
                        return None
            except Exception as e:
                if attempt < max_retries:
                    delay = retry_delays[attempt]
                    print(f"[YoFreeSamples] Attempt {attempt + 1} failed, retrying in {delay}s: {e}")
                    await asyncio.sleep(delay)
                else:
                    print(f"[YoFreeSamples] Failed after {max_retries} attempts: {e}")
                    self.stats["errors"] += 1
                    return None

    async def _scrape_courses(self):
        async with aiohttp.ClientSession() as session:
            for page in range(1, self.pages + 1):
                url = f"{self.base_url}?page={page}" if page > 1 else self.base_url
                response = await self._make_request_with_retry(session, url)
                if not response:
                    continue
                try:
                    soup = BeautifulSoup(response, 'html5lib')
                    course_blocks = soup.find_all('div', class_='wp-block-kadence-rowlayout')
                    for block in course_blocks:
                        try:
                            # Title
                            title = None
                            title_elem = block.find('h4', class_='wp-block-heading')
                            if title_elem:
                                a_title = title_elem.find('a')
                                if a_title:
                                    title = a_title.get_text(strip=True)
                            # Udemy link
                            udemy_link = None
                            a_button = block.find('a', class_='external_link_button')
                            if a_button and a_button.has_attr('href'):
                                udemy_link = a_button['href']
                            else:
                                if title_elem and a_title and a_title.has_attr('href'):
                                    udemy_link = a_title['href']
                            # Coupon code
                            coupon_code = None
                            for p in block.find_all('p'):
                                if 'Coupon:' in p.get_text():
                                    text = p.get_text()
                                    match = re.search(r'Coupon:\s*([A-Z0-9]+)', text)
                                    if match:
                                        coupon_code = match.group(1)
                                    break
                            # Current price, previous price, rating, category
                            current_price = "FREE"
                            previous_price = "Unknown"
                            rating = "4.5"
                            category = "Unknown"
                            for p in block.find_all('p'):
                                text = p.get_text()
                                if 'Current Price:' in text:
                                    match = re.search(r'Current Price:\s*([^\s]+)', text)
                                    if match:
                                        current_price = match.group(1)
                                if 'Previous Price:' in text:
                                    match = re.search(r'Previous Price:\s*([^\s]+)', text)
                                    if match:
                                        previous_price = match.group(1)
                                if 'Rating:' in text:
                                    match = re.search(r'Rating:\s*([0-9.]+)', text)
                                    if match:
                                        rating = match.group(1)
                                if 'Category:' in text:
                                    match = re.search(r'Category:\s*([\w &-]+)', text)
                                    if match:
                                        category = match.group(1)
                           # Image URL
                            image_url = "Unknown"
                            figure = block.find('figure')
                            if figure:
                                img = figure.find('img')
                                if img:
                                    # Check for data-lazy-src first (more likely to be the real image)
                                    if img.has_attr('data-lazy-src'):
                                        image_url = img['data-lazy-src']
                                    elif img.has_attr('src'):
                                        image_url = img['src']

                            # Other fields
                            students = "Unknown"
                            language = "Unknown"
                            badge = "Unknown"
                            discount_time_left = "Unknown"
                            source = "YoFreeSamples"
                            # Only add if all required fields are present
                            if title and udemy_link and coupon_code:
                                course_obj = course.Course(
                                    id=None,
                                    title=title,
                                    link=udemy_link,
                                    coupon_code=coupon_code,
                                    date_found=time.strftime("%Y-%m-%d %H:%M:%S"),
                                    current_price=current_price,
                                    previous_price=previous_price,
                                    rating=rating,
                                    category=category,
                                    image_url=image_url,
                                    students=students,
                                    language=language,
                                    badge=badge,
                                    discount_time_left=discount_time_left,
                                    source=source
                                )
                                self.courses.append(course_obj)
                                self.stats["added"] += 1
                                self.stats["total_found"] += 1
                            else:
                                print(f"[YoFreeSamples] Skipped block (missing data): title={title}, link={udemy_link}, coupon={coupon_code}")
                        except Exception as e:
                            print(f"[YoFreeSamples] Error parsing course block: {e}")
                            self.stats["errors"] += 1
                except Exception as e:
                    print(f"[YoFreeSamples] Error parsing page {page}: {e}")
                    self.stats["errors"] += 1
        print(f"[YoFreeSamples] Total courses found: {self.stats['total_found']}")


class StatsScraper:
    def get_stats(self, course_link):
        # This is a placeholder - you can implement course stats scraping if needed
        return {
            "rating": "4.5",
            "students": "1.2k",
            "language": "English",
            "discount_time_left": "2 days",
            "badge": "Bestseller"
        }


class RealDiscountScraper(_CoursesScraper):
    def __init__(self, pages):
        super().__init__()
        self.pages = pages
        self.api_url = "https://cdn.real.discount/api/courses"
        self.base_url = "https://real.discount"

    def find_courses(self):
        print(f"[RealDiscount] Scraping {self.pages} pages...")
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self._scrape_courses())
        finally:
            loop.close()

    async def _check_network_connectivity(self, session):
        try:
            async with session.get("https://httpbin.org/get", timeout=10) as response:
                return response.status == 200
        except:
            return False

    async def _make_request_with_retry(self, session, url, headers, page_num):
        max_retries = 3
        retry_delays = [2, 5, 10]

        for attempt in range(max_retries + 1):
            try:
                async with session.get(url, headers=headers, timeout=30) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"[RealDiscount] Page {page_num} returned status {response.status}")
                        return None
            except Exception as e:
                if attempt < max_retries:
                    delay = retry_delays[attempt]
                    print(f"[RealDiscount] Attempt {attempt + 1} failed for page {page_num}, retrying in {delay}s: {e}")
                    await asyncio.sleep(delay)
                else:
                    print(f"[RealDiscount] Failed to fetch page {page_num} after {max_retries} attempts: {e}")
                    self.stats["errors"] += 1
                    return None

    async def _scrape_courses(self):
        async with aiohttp.ClientSession() as session:
            # Check network connectivity
            if not await self._check_network_connectivity(session):
                print("[RealDiscount] Network connectivity check failed")
                return

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }

            for page in range(1, self.pages + 1):
                url = f"{self.api_url}?page={page}"
                
                response_data = await self._make_request_with_retry(session, url, headers, page)
                if not response_data:
                    continue

                try:
                    courses_data = response_data.get("courses", [])
                    
                    for course_data in courses_data:
                        try:
                            # Check if course is free
                            sale_price = course_data.get("sale_price", 0)
                            if sale_price != 0:
                                continue

                            title = course_data.get("title", "")
                            udemy_link = course_data.get("udemy_link", "")
                            coupon_code = course_data.get("coupon_code", "")

                            if not title or not udemy_link or not coupon_code:
                                continue

                            # Validate coupon
                            if await self._is_coupon_valid(session, udemy_link):
                                self._add_course(title, udemy_link)
                                self.stats["total_found"] += 1

                        except Exception as e:
                            print(f"[RealDiscount] Error processing course: {e}")
                            self.stats["errors"] += 1

                except Exception as e:
                    print(f"[RealDiscount] Error parsing page {page}: {e}")
                    self.stats["errors"] += 1

    async def _is_coupon_valid(self, session, udemy_link):
        try:
            headers = self.get_random_headers()
            async with session.get(udemy_link, headers=headers, timeout=30) as response:
                return response.status == 200
        except:
            return False

    def _print_analytics(self):
        print(f"\n📊 RealDiscount Analytics:")
        print(f"   Total found: {self.stats['total_found']}")
        print(f"   Added: {self.stats['added']}")
        print(f"   Skipped (no coupon): {self.stats['skipped_no_coupon']}")
        print(f"   Skipped (duplicate): {self.stats['skipped_duplicate_coupon']}")
        print(f"   Errors: {self.stats['errors']}")
