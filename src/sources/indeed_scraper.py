import time
from pprint import pprint
from urllib.parse import quote_plus, parse_qs, urlparse
from playwright.sync_api import sync_playwright
from config.indeed_scraper_config import indeed_scraper_config


class IndeedScraper:
    def __init__(self):
        self.query_urls = None
        self.all_query_matched_job_urls = None
        self.all_query_matched_jobs = None # scrape job descriptions and construct list of JOB objects
        self.matching_jobs = None # Resume matching jobs in embedding space --> save these jobs into db immediately
        self.db_saved_jobs = None # Successfully saved jobs to the DB


    def run_scraper(self):
        # TODO: Surround following block with if to disable scraper
        self.query_urls = self.build_query_urls()
        print(len(self.query_urls))
        print(self.query_urls)
        self.all_query_matched_job_urls = self.extract_job_urls(self.query_urls)
        print(len(self.all_query_matched_job_urls))
        print(self.all_query_matched_job_urls)



    @staticmethod
    def build_query_urls() -> list[str]:
        urls = []
        location_radius_pairs = indeed_scraper_config["location_radius_pairs"]
        keywords_list = indeed_scraper_config["search_keywords"]
        job_age = indeed_scraper_config["job_age"]
        base_url = indeed_scraper_config["BASE_URL"]
        for k,v in location_radius_pairs.items():
            for kw in keywords_list:
                kw = kw.strip()
                k = k.strip()
                url = base_url.format(
                    keywords=quote_plus(kw),
                    location=quote_plus(k),
                    radius=v,
                    job_age=job_age,
                )
                urls.append(url)
        return urls


    def extract_job_urls(self, query_url_list:list[str]) -> set[str]:
        job_urls = set()
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=indeed_scraper_config["use_headless_mode"], # Headless scraping is not allowed on xing
            )
            page = browser.new_page()
            for url in query_url_list:
                print(url)
                page.goto(url)
                reject_cookies = page.locator("button[id='onetrust-reject-all-handler']")
                reject_cookies.click() # reject cookies
                page.wait_for_selector("div[class*='jobsearch-LeftPane']")
                empty_result = page.locator("div[class*='jobsearch-NoResult-messageContainer']").is_visible()
                if empty_result:
                    print(f"No results found for query {url}")
                    continue
                cards = page.locator("#mosaic-jobResults #mosaic-provider-jobcards ul > li[class*='css']  a[id*='job']") # > div[class*='vjs-highlight']
                print(cards.count())
                for i in range(cards.count()):
                    card = cards.nth(i)
                    href = card.get_attribute("href")
                    if href:
                        if href.startswith("/rc/clk?"): # only allow valid hrefs
                            full_url = self.normalize_indeed_url("https://de.indeed.com/viewjob?"+ href[8:len(href)]) # construct full_url by removing "/rc/clk?"
                            # Example of href scraped from HTML: "/rc/clk?jk=7d79172975914a6c&bb=r6STzscjGymbQadnjPTxYUuqozf0DHAMtElUW1i-8QubawdLKL7PNk7qHQixZLOmLO8txAQbl6aGauzPwr5RmJ9qfLu45DUHWGh48l7WOW8mIynrK5nb77Q3GAeVHwaS&xkcb=SoCm67M3hFOv3FzNV50LbzkdCdPP&fccid=6a9687b53c8c4525&cmp=eiei-4-einzelhandel-gmbh&ti=IT+Manager&vjs=3"
                            job_urls.add(full_url)
                page.close()
                page = browser.new_page()
            browser.close()
        return job_urls


    @staticmethod
    def normalize_indeed_url(url: str) -> str:
        query = parse_qs(urlparse(url).query)
        job_id = query.get("jk", [None])[0]
        if not job_id:
            return url
        return f"https://de.indeed.com/viewjob?jk={job_id}"


if __name__=="__main__":
    indeed_scraper = IndeedScraper()
    indeed_scraper.run_scraper()



'''
from pprint import pprint
from urllib.parse import parse_qs, quote_plus, urlparse

from playwright.sync_api import sync_playwright

from config.indeed_scraper_config import indeed_scraper_config
from src.utils.browser_session import BrowserSession
from src.utils.logger import logger


def build_query_urls() -> list[str]:
    urls = []

    for location, radius in indeed_scraper_config["location_radius_pairs"].items():

        for keyword in indeed_scraper_config["search_keywords"]:

            urls.append(
                indeed_scraper_config["BASE_URL"].format(
                    keywords=quote_plus(keyword.strip()),
                    location=quote_plus(location.strip()),
                    radius=radius,
                    job_age=indeed_scraper_config["job_age"],
                )
            )
    logger.info(f"[Indeed Scraper] Built query set contains {len(urls)} URLs.")
    logger.info(f"[Indeed Scraper] URLs are: {urls}")
    return urls


def extract_job_urls(query_urls: list[str]) -> set[str]:

    job_urls = set()

    with sync_playwright() as p:

        with BrowserSession(
            playwright=p,
            scraper_name="Indeed",
            headless=False,
        ) as session:

            for url in query_urls:

                logger.info(f"Searching {url}")

                page = session.new_page()

                try:

                    page.goto(url)

                    reject = page.locator("#onetrust-reject-all-handler")

                    if reject.is_visible():
                        reject.click()

                    page.wait_for_selector(
                        "div[class*=jobsearch-LeftPane]"
                    )

                    if page.locator(
                        "div[class*=jobsearch-NoResult-messageContainer]"
                    ).is_visible():

                        logger.warning(f"No results for {url}")
                        continue

                    cards = page.locator(
                        "#mosaic-jobResults "
                        "#mosaic-provider-jobcards "
                        "ul > li[class*=css] "
                        "a[id*=job]"
                    )

                    logger.info(f"Found {cards.count()} jobs")

                    for i in range(cards.count()):

                        href = cards.nth(i).get_attribute("href")

                        if href and href.startswith("/rc/clk?"):

                            job_urls.add(
                                normalize_indeed_url(
                                    "https://de.indeed.com/viewjob?"
                                    + href[8:]
                                )
                            )

                finally:
                     page.close()

    return job_urls


def normalize_indeed_url(url: str) -> str:
    query = parse_qs(urlparse(url).query)
    job_id = query.get("jk", [None])[0]

    if not job_id:
        return url

    return f"https://de.indeed.com/viewjob?jk={job_id}"


if __name__ == "__main__":

    jobs = extract_job_urls(build_query_urls())

    logger.info(f"Collected {len(jobs)} jobs")

    pprint(jobs)
'''