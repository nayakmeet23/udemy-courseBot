import re
import aiohttp
import asyncio
from lxml import html
from datetime import datetime
from abc import ABC, abstractmethod
import random
from urllib.parse import urlparse, parse_qs


class _CoursesScraper(ABC):
    HEADERS_LIST = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) Version/14.0 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    ]

    def __init__(self):
        self.courses = []
        self.date = None
        # Analytics tracking
        self.stats = {
            'total_found': 0,
            'skipped_duplicate_link': 0,
            'skipped_no_coupon': 0,
            'skipped_invalid_data': 0,
            'added': 0,
            'errors': 0
        }
        # Track skipped courses for reporting
        self.skipped_courses = []

    def get_random_headers(self):
        return {
            "User-Agent": random.choice(self.HEADERS_LIST),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }

    @abstractmethod
    def find_courses(self) -> None:
        pass

    def _add_course(self, title, link):
        if any(d["link"] == link for d in self.courses):
            self.skipped_courses.append({
                'title': title,
                'website': self.__class__.__name__.replace('Scraper', ''),
                'reason': 'Duplicate link'
            })
            self.stats['skipped_duplicate_link'] += 1
            return
        
        # Extract coupon code from the link using proper URL parsing
        coupon_code = "Unknown"
        try:
            parsed_url = urlparse(link)
            query_params = parse_qs(parsed_url.query)
            if 'couponCode' in query_params:
                coupon_code = query_params['couponCode'][0]
                # Clean up the coupon code - remove any trailing &couponCode
                if coupon_code.endswith('&couponCode'):
                    coupon_code = coupon_code.replace('&couponCode', '')
        except Exception:
            # Fallback: try old method
            link_parts = link.split("/?")
            if len(link_parts) < 2:
                self.skipped_courses.append({
                    'title': title,
                    'website': self.__class__.__name__.replace('Scraper', ''),
                    'reason': 'Invalid data'
                })
                self.stats['skipped_invalid_data'] += 1
                return
            try:
                coupon_code = link_parts[1].split("=")[1]
                # Clean up the coupon code - remove any trailing &couponCode
                if coupon_code.endswith('&couponCode'):
                    coupon_code = coupon_code.replace('&couponCode', '')
            except IndexError:
                coupon_code = "Unknown"
        
        if not coupon_code or coupon_code == "Unknown":
            self.skipped_courses.append({
                'title': title,
                'website': self.__class__.__name__.replace('Scraper', ''),
                'reason': 'No coupon code'
            })
            self.stats['skipped_no_coupon'] += 1
            return
        
        self.courses.append({
            "title": title.strip(),
            "link": link,  # Store the full link with coupon code
            "coupon_code": coupon_code,
            "date_found": self.date,
        })
        self.stats['added'] += 1

    def print_analytics(self, scraper_name):
        """Print analytics for this scraper"""
        print(f"\n📊 {scraper_name} Analytics")
        print("-" * 40)
        print(f"Total courses found: {self.stats.get('total_found', 0)}")
        print(f"✅ Successfully added: {self.stats.get('added', 0)}")
        print(f"❌ Skipped duplicate link: {self.stats.get('skipped_duplicate_link', 0)}")
        print(f"❌ Skipped no coupon: {self.stats.get('skipped_no_coupon', 0)}")
        print(f"❌ Skipped invalid data: {self.stats.get('skipped_invalid_data', 0)}")
        print(f"❌ Skipped ads/sponsored: {self.stats.get('skipped_ads', 0)}")
        print(f"❌ Skipped non-Udemy: {self.stats.get('skipped_non_udemy', 0)}")
        print(f"❌ Skipped not free: {self.stats.get('skipped_not_free', 0)}")
        print(f"❌ Skipped duplicate coupon: {self.stats.get('skipped_duplicate_coupon', 0)}")
        print(f"❌ Skipped expired: {self.stats.get('skipped_expired', 0)}")
        print(f"⚠️  Errors encountered: {self.stats.get('errors', 0)}")
        
        total_found = self.stats.get('total_found', 0)
        if total_found > 0:
            success_rate = (self.stats.get('added', 0) / total_found) * 100
            print(f"📈 Success rate: {success_rate:.1f}%")
        print("-" * 40)


class DiscudemyScraper(_CoursesScraper):
    def __init__(self, pages):
        super().__init__()
        self.pages = pages
        self.base_url = "https://www.discudemy.com"
        self.all_links = []
        self.loop = asyncio.get_event_loop()
        # Retry configuration
        self.max_retries = 2
        self.retry_delays = [1, 3]  # Shorter delays for Discudemy
        self.loop.run_until_complete(self._fetch_all_course_links())

    async def _make_request_with_retry(self, session, url, page_num):
        """Make HTTP request with retry logic for Discudemy"""
        for attempt in range(self.max_retries + 1):
            try:
                timeout = 10 + (attempt * 2)  # Increase timeout with each retry
                async with session.get(url, headers=self.get_random_headers(), timeout=aiohttp.ClientTimeout(total=timeout), ssl=False) as resp:
                    if resp.status == 200:
                        return await resp.read()
                    else:
                        print(f"[Retry {attempt + 1}] HTTP {resp.status} for page {page_num}")
                        self.stats['errors'] += 1
                        
            except asyncio.TimeoutError:
                print(f"[Retry {attempt + 1}] Timeout for page {page_num} (timeout: {timeout}s)")
                if attempt < self.max_retries:
                    delay = self.retry_delays[attempt]
                    print(f"[Retry {attempt + 1}] Waiting {delay}s before retry...")
                    await asyncio.sleep(delay)
                else:
                    print(f"[Final] Failed after {self.max_retries + 1} attempts for page {page_num}")
                    self.stats['errors'] += 1
                    return None
                    
            except Exception as e:
                print(f"[Retry {attempt + 1}] Error for page {page_num}: {e}")
                if attempt < self.max_retries:
                    delay = self.retry_delays[attempt]
                    print(f"[Retry {attempt + 1}] Waiting {delay}s before retry...")
                    await asyncio.sleep(delay)
                else:
                    print(f"[Final] Failed after {self.max_retries + 1} attempts for page {page_num}")
                    self.stats['errors'] += 1
                    return None
        
        return None

    async def _fetch_all_course_links(self):
        async with aiohttp.ClientSession() as session:
            for page in range(1, self.pages + 1):
                url = f"{self.base_url}/all/{page}"
                print(f"[Debug] Attempting to fetch: {url}")
                
                content = await self._make_request_with_retry(session, url, page)
                if content is None:
                    continue
                
                print(f"[Debug] Response status: 200")
                doc = html.fromstring(content)
                links_found = doc.xpath('//a[@class="card-header"]/@href')
                self.all_links.extend(links_found)
                self.stats['total_found'] += len(links_found)
                print(f"[Debug] Found {len(links_found)} course links on page {page}")
                await asyncio.sleep(random.uniform(0.2, 0.5))  # Reduced delay

    def find_courses(self):
        self.loop.run_until_complete(self._scrape_course_details())
        self.print_analytics("DiscudemyScraper")

    async def _scrape_course_details(self):
        self.courses = []
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Limit the number of courses to process for faster execution
        from udemypy.udemy import settings
        max_courses_to_process = settings.MAX_COURSES_TO_PROCESS if settings.FAST_MODE else len(self.all_links)
        limited_links = self.all_links[:max_courses_to_process]
        
        print(f"[Scraper] Processing {len(limited_links)} courses out of {len(self.all_links)} found")
        
        async with aiohttp.ClientSession() as session:
            # Process courses with limited concurrency
            semaphore = asyncio.Semaphore(5)  # Max 5 concurrent requests
            
            async def process_course(course_url):
                async with semaphore:
                    try:
                        async with session.get(course_url, headers=self.get_random_headers(), timeout=aiohttp.ClientTimeout(total=8), ssl=False) as resp:
                            detail_doc = html.fromstring(await resp.read())
                            go_links = detail_doc.xpath('//a[contains(@class, "discBtn")]/@href')
                            if not go_links:
                                self.skipped_courses.append({
                                    'title': course_url.split("/")[-1].replace("-", " ").capitalize(),
                                    'website': 'Discudemy',
                                    'reason': 'No go link found'
                                })
                                return
                            async with session.get(go_links[0], headers=self.get_random_headers(), timeout=aiohttp.ClientTimeout(total=8), ssl=False) as go_resp:
                                go_doc = html.fromstring(await go_resp.read())
                                udemy_links = go_doc.xpath('//p[contains(text(),"Course Coupon:")]/following-sibling::a[1]/@href')
                                if udemy_links and "udemy.com" in udemy_links[0]:
                                    title = course_url.split("/")[-1].replace("-", " ").capitalize()
                                    self._add_course(title, udemy_links[0])
                                else:
                                    self.skipped_courses.append({
                                        'title': course_url.split("/")[-1].replace("-", " ").capitalize(),
                                        'website': 'Discudemy',
                                        'reason': 'No Udemy link found'
                                    })
                            await asyncio.sleep(random.uniform(0.1, 0.3))  # Reduced delay
                    except Exception as e:
                        self.skipped_courses.append({
                            'title': course_url.split("/")[-1].replace("-", " ").capitalize() if course_url else 'Unknown',
                            'website': 'Discudemy',
                            'reason': f'Error: {str(e)}'
                        })
                        print(f"[!] Failed to extract course from {course_url}: {e}")
                        self.stats['errors'] += 1
            
            # Process courses concurrently
            tasks = [process_course(course_url) for course_url in limited_links]
            await asyncio.gather(*tasks)


class YoFreeSamplesScraper(_CoursesScraper):
    def __init__(self, pages):
        super().__init__()
        self.pages = pages
        self.base_url = "https://yofreesamples.com/courses/free-discounted-udemy-courses-list/"
        self.loop = asyncio.get_event_loop()
        # Retry configuration
        self.max_retries = 2
        self.retry_delays = [1, 3]  # Shorter delays for YoFreeSamples

    def find_courses(self):
        self.loop.run_until_complete(self._scrape_courses())
        self.print_analytics("YoFreeSamplesScraper")

    async def _make_request_with_retry(self, session, url):
        """Make HTTP request with retry logic for YoFreeSamples"""
        for attempt in range(self.max_retries + 1):
            try:
                timeout = 15 + (attempt * 3)  # Increase timeout with each retry
                async with session.get(url, headers=self.get_random_headers(), timeout=aiohttp.ClientTimeout(total=timeout), ssl=False) as resp:
                    if resp.status == 200:
                        return await resp.read()
                    else:
                        print(f"[Retry {attempt + 1}] HTTP {resp.status} for YoFreeSamples")
                        self.stats['errors'] += 1
                        
            except asyncio.TimeoutError:
                print(f"[Retry {attempt + 1}] Timeout for YoFreeSamples (timeout: {timeout}s)")
                if attempt < self.max_retries:
                    delay = self.retry_delays[attempt]
                    print(f"[Retry {attempt + 1}] Waiting {delay}s before retry...")
                    await asyncio.sleep(delay)
                else:
                    print(f"[Final] Failed after {self.max_retries + 1} attempts for YoFreeSamples")
                    self.stats['errors'] += 1
                    return None
                    
            except Exception as e:
                print(f"[Retry {attempt + 1}] Error for YoFreeSamples: {e}")
                if attempt < self.max_retries:
                    delay = self.retry_delays[attempt]
                    print(f"[Retry {attempt + 1}] Waiting {delay}s before retry...")
                    await asyncio.sleep(delay)
                else:
                    print(f"[Final] Failed after {self.max_retries + 1} attempts for YoFreeSamples")
                    self.stats['errors'] += 1
                    return None
        
        return None

    async def _scrape_courses(self):
        self.courses = []
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[YoFreeSamples Scraper] Starting to scrape courses...")
        print(f"[Debug] Attempting to fetch: {self.base_url}")
        async with aiohttp.ClientSession() as session:
            content = await self._make_request_with_retry(session, self.base_url)
            if content is None:
                return
            
            print(f"[Debug] YoFreeSamples response status: 200")
            doc = html.fromstring(content)

            # Find all course containers
            course_containers = doc.xpath('//div[contains(@class, "wp-block-kadence-rowlayout")]')
            print(f"[YoFreeSamples Scraper] Found {len(course_containers)} course containers")
            self.stats['total_found'] = len(course_containers)

            from udemypy.udemy import settings
            max_courses_to_process = settings.MAX_COURSES_TO_PROCESS if settings.FAST_MODE else len(course_containers)
            limited_containers = course_containers[:max_courses_to_process]

            for container in limited_containers:
                try:
                    # Title and Udemy link
                    title_elem = container.xpath('.//a[contains(@class, "external_link_title")]')
                    if not title_elem:
                        continue
                    title = title_elem[0].text_content().strip()
                    udemy_link = title_elem[0].get('href')
                    if not title or not udemy_link or 'udemy.com' not in udemy_link:
                        self.skipped_courses.append({
                            'title': title if title else 'Unknown',
                            'website': 'YoFreeSamples',
                            'reason': 'Invalid title or link'
                        })
                        continue

                    # Extract coupon code from the Udemy link using proper URL parsing
                    coupon_code = "Unknown"
                    try:
                        parsed_url = urlparse(udemy_link)
                        query_params = parse_qs(parsed_url.query)
                        if 'couponCode' in query_params:
                            coupon_code = query_params['couponCode'][0]
                    except Exception:
                        # Fallback: try to extract from text content
                        text_content = container.text_content()
                        coupon_match = re.search(r'Coupon:\s*([A-Z0-9_]+)', text_content)
                        if coupon_match:
                            coupon_code = coupon_match.group(1)
                    
                    if not coupon_code or coupon_code == "Unknown":
                        self.skipped_courses.append({
                            'title': title,
                            'website': 'YoFreeSamples',
                            'reason': 'No coupon code found'
                        })
                        continue

                    # Compose the full Udemy link with coupon
                    if "?" in udemy_link:
                        # Check if coupon code is already in the URL
                        if f"couponCode={coupon_code}" in udemy_link:
                            full_link = udemy_link
                        else:
                            full_link = f"{udemy_link}&couponCode={coupon_code}"
                    else:
                        full_link = f"{udemy_link}?couponCode={coupon_code}"

                    self._add_course(title, full_link)
                except Exception as e:
                    self.skipped_courses.append({
                        'title': 'Unknown',
                        'website': 'YoFreeSamples',
                        'reason': f'Error: {str(e)}'
                    })
                    self.stats['errors'] += 1
                    continue
            print(f"[YoFreeSamples Scraper] Successfully extracted {len(self.courses)} courses")


class StatsScraper:
    def get_stats(self, course_link):
        return {
            "id": "Unknown",
            "discount": 100,  # DiscUdemy courses are typically free (100% discount)
            "discount_time_left": "Unknown",
            "rating": "Unknown",
            "students": "Unknown",
            "language": "Unknown",
            "badge": "Unknown",
        }


class RealDiscountScraper(_CoursesScraper):
    def __init__(self, pages):
        super().__init__()
        self.pages = pages
        self.api_base_url = "https://cdn.real.discount/api/courses"
        self.loop = asyncio.get_event_loop()
        # Analytics tracking
        self.stats = {
            'total_found': 0,
            'skipped_ads': 0,
            'skipped_non_udemy': 0,
            'skipped_not_free': 0,
            'skipped_no_coupon': 0,
            'skipped_duplicate_coupon': 0,
            'skipped_expired': 0,
            'added': 0,
            'errors': 0,
            'retries': 0,
            'timeouts': 0
        }
        # Track skipped courses for reporting
        self.skipped_courses = []
        # Retry configuration
        self.max_retries = 3
        self.base_timeout = 30  # Increased from 15 to 30 seconds
        self.retry_delays = [2, 5, 10]  # Exponential backoff delays

    def find_courses(self):
        self.loop.run_until_complete(self._scrape_courses())
        self._print_analytics()

    async def _check_network_connectivity(self, session):
        """Check if RealDiscount API is accessible"""
        try:
            test_url = "https://cdn.real.discount/api/courses?page=1&limit=1"
            async with session.get(test_url, timeout=aiohttp.ClientTimeout(total=10), ssl=False) as resp:
                return resp.status == 200
        except Exception as e:
            print(f"[Network Check] RealDiscount API not accessible: {e}")
            return False

    async def _make_request_with_retry(self, session, url, headers, page_num):
        """Make HTTP request with retry logic and exponential backoff"""
        for attempt in range(self.max_retries + 1):
            try:
                timeout = self.base_timeout + (attempt * 5)  # Increase timeout with each retry
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=timeout), ssl=False) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        print(f"[Retry {attempt + 1}] HTTP {resp.status} for page {page_num}")
                        self.stats['errors'] += 1
                        
            except asyncio.TimeoutError:
                self.stats['timeouts'] += 1
                print(f"[Retry {attempt + 1}] Timeout for page {page_num} (timeout: {timeout}s)")
                if attempt < self.max_retries:
                    delay = self.retry_delays[attempt]
                    print(f"[Retry {attempt + 1}] Waiting {delay}s before retry...")
                    await asyncio.sleep(delay)
                else:
                    print(f"[Final] Failed after {self.max_retries + 1} attempts for page {page_num}")
                    self.stats['errors'] += 1
                    return None
                    
            except Exception as e:
                print(f"[Retry {attempt + 1}] Error for page {page_num}: {e}")
                if attempt < self.max_retries:
                    delay = self.retry_delays[attempt]
                    print(f"[Retry {attempt + 1}] Waiting {delay}s before retry...")
                    await asyncio.sleep(delay)
                else:
                    print(f"[Final] Failed after {self.max_retries + 1} attempts for page {page_num}")
                    self.stats['errors'] += 1
                    return None
        
        return None

    async def _scrape_courses(self):
        self.courses = []
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[RealDiscount Scraper] Starting to scrape courses...")
        
        # Track used coupon codes to avoid duplicates
        used_coupon_codes = set()
        
        async with aiohttp.ClientSession() as session:
            # Check network connectivity first
            print("[Network Check] Testing RealDiscount API connectivity...")
            if not await self._check_network_connectivity(session):
                print("[Network Check] ❌ RealDiscount API is not accessible. Skipping RealDiscount scraper.")
                self.stats['errors'] += 1
                return
            print("[Network Check] ✅ RealDiscount API is accessible.")
            
            for page in range(1, self.pages + 1):
                try:
                    url = f"{self.api_base_url}?page={page}&limit=14&sortBy=sale_start"
                    print(f"[Debug] Attempting to fetch RealDiscount API: {url}")
                    
                    headers = {
                        "accept": "*/*",
                        "accept-language": "en-US,en;q=0.8",
                        "origin": "https://real.discount",
                        "referer": "https://real.discount/",
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
                    }
                    
                    # Use retry mechanism
                    data = await self._make_request_with_retry(session, url, headers, page)
                    if data is None:
                        continue
                    
                    print(f"[Debug] RealDiscount API response status: 200")
                    print(f"[Debug] RealDiscount API raw response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                    print(f"[Debug] RealDiscount API response type: {type(data)}")
                    
                    courses_data = data.get('items', []) if isinstance(data, dict) else data
                    print(f"[Debug] Found {len(courses_data)} courses on page {page}")
                    
                    for course in courses_data:
                        try:
                            self.stats['total_found'] += 1
                            title = course.get("name", "").strip()
                            
                            # Skip ads and sponsored content
                            if course.get("type") == "ad" or course.get("store") == "Sponsored":
                                self.skipped_courses.append({
                                    'title': title,
                                    'website': 'RealDiscount',
                                    'reason': 'Ad/Sponsored content'
                                })
                                self.stats['skipped_ads'] += 1
                                continue
                            
                            # Skip non-Udemy courses
                            if course.get("store") != "Udemy":
                                self.skipped_courses.append({
                                    'title': title,
                                    'website': 'RealDiscount',
                                    'reason': f'Non-Udemy course (Store: {course.get("store", "Unknown")})'
                                })
                                self.stats['skipped_non_udemy'] += 1
                                continue
                            
                            # Filter for only truly free courses
                            if course.get("sale_price", 1) != 0:
                                self.skipped_courses.append({
                                    'title': title,
                                    'website': 'RealDiscount',
                                    'reason': f'Not free (Price: {course.get("sale_price", "Unknown")})'
                                })
                                self.stats['skipped_not_free'] += 1
                                continue
                            
                            udemy_link = course.get("url", "")
                            
                            if not title or not udemy_link or "udemy.com" not in udemy_link:
                                self.skipped_courses.append({
                                    'title': title,
                                    'website': 'RealDiscount',
                                    'reason': 'Invalid course data'
                                })
                                self.stats['errors'] += 1
                                continue
                            
                            # Extract coupon code from the Udemy link
                            coupon_code = "Unknown"
                            if "couponCode=" in udemy_link:
                                coupon_code = udemy_link.split("couponCode=")[1].split("&")[0]
                            
                            if not coupon_code or coupon_code == "Unknown":
                                self.skipped_courses.append({
                                    'title': title,
                                    'website': 'RealDiscount',
                                    'reason': 'No coupon code'
                                })
                                self.stats['skipped_no_coupon'] += 1
                                continue
                            
                            # Check for duplicate coupon codes across sources
                            if coupon_code in used_coupon_codes:
                                self.skipped_courses.append({
                                    'title': title,
                                    'website': 'RealDiscount',
                                    'reason': f'Duplicate coupon code: {coupon_code}'
                                })
                                self.stats['skipped_duplicate_coupon'] += 1
                                continue
                            
                            # Optional: Check if coupon is still valid (headless request)
                            if await self._is_coupon_valid(session, udemy_link):
                                used_coupon_codes.add(coupon_code)
                                self._add_course(title, udemy_link)
                                self.stats['added'] += 1
                            else:
                                self.skipped_courses.append({
                                    'title': title,
                                    'website': 'RealDiscount',
                                    'reason': 'Expired coupon'
                                })
                                self.stats['skipped_expired'] += 1
                            
                        except Exception as e:
                            self.skipped_courses.append({
                                'title': title if 'title' in locals() else 'Unknown',
                                'website': 'RealDiscount',
                                'reason': f'Error: {str(e)}'
                            })
                            self.stats['errors'] += 1
                            continue
                    
                    # Rate limiting - respect API limits
                    await asyncio.sleep(random.uniform(1.0, 2.0))  # Increased delay between pages
                    
                except Exception as e:
                    print(f"[!] Failed to load RealDiscount page {page}")
                    print(f"[Debug] Exception type: {type(e).__name__}")
                    print(f"[Debug] Exception message: {str(e)}")
                    
                    # Add specific error tracking
                    if isinstance(e, asyncio.TimeoutError):
                        print(f"[Debug] Timeout occurred for page {page} - consider increasing timeout or reducing rate")
                    elif isinstance(e, aiohttp.ClientError):
                        print(f"[Debug] Network error for page {page} - check internet connection")
                    
                    self.stats['errors'] += 1
        
        print(f"[RealDiscount Scraper] Successfully extracted {len(self.courses)} courses")

    async def _is_coupon_valid(self, session, udemy_link):
        """Check if the coupon is still valid by making a headless request"""
        try:
            async with session.head(udemy_link, timeout=aiohttp.ClientTimeout(total=5), ssl=False) as resp:
                # If we get a 200 status, the coupon is likely still valid
                # If we get a 404 or other error, the coupon might be expired
                return resp.status == 200
        except Exception:
            # If we can't check, assume it's valid
            return True

    def _print_analytics(self):
        """Print detailed analytics about the scraping process"""
        print("\n" + "="*60)
        print("📊 RealDiscount Scraper Analytics")
        print("="*60)
        print(f"Total courses found: {self.stats['total_found']}")
        print(f"✅ Successfully added: {self.stats['added']}")
        print(f"❌ Skipped ads/sponsored: {self.stats['skipped_ads']}")
        print(f"❌ Skipped non-Udemy: {self.stats['skipped_non_udemy']}")
        print(f"❌ Skipped not free: {self.stats['skipped_not_free']}")
        print(f"❌ Skipped no coupon: {self.stats['skipped_no_coupon']}")
        print(f"❌ Skipped duplicate coupon: {self.stats['skipped_duplicate_coupon']}")
        print(f"❌ Skipped expired: {self.stats['skipped_expired']}")
        print(f"⚠️  Errors encountered: {self.stats['errors']}")
        print(f"🔄 Retries attempted: {self.stats['retries']}")
        print(f"⏱️  Timeouts occurred: {self.stats['timeouts']}")
        
        if self.stats['total_found'] > 0:
            success_rate = (self.stats['added'] / self.stats['total_found']) * 100
            print(f"📈 Success rate: {success_rate:.1f}%")
        print("="*60)


__all__ = ["DiscudemyScraper", "YoFreeSamplesScraper", "RealDiscountScraper", "StatsScraper"]
