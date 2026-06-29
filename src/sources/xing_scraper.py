import time
from pprint import pprint
from playwright.sync_api import sync_playwright
from config.xing_scraper_config import xing_scraper_config


class XingScraper:
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
        location_radius_pairs = xing_scraper_config["location_radius_pairs"]
        keywords_list = xing_scraper_config["search_keywords"]
        job_age = xing_scraper_config["job_age"]
        base_url = xing_scraper_config["BASE_URL"]
        for k,v in location_radius_pairs.items():
            for kw in keywords_list:
                kw = kw.strip().lower().replace(" ", "%20")
                k = k.strip().replace(" ", "%20")
                url = base_url.format(
                    keywords=kw,
                    location=k,
                    radius=v,
                    job_age=job_age,
                )
                urls.append(url)
        return urls


    @staticmethod
    def extract_job_urls(query_url_list:list[str]) -> set[str]:
        job_urls = set()
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=xing_scraper_config["use_headless_mode"], # Headless scraping is not allowed on xing
            )
            page = browser.new_page()
            for url in query_url_list:
                print(url)
                page.goto(url)
                accept = page.locator("button[data-action-type='accept'][id='accept']")
                accept.click() # accept cookies
                page.wait_for_selector("div[class*='container__Container']")
                cards = page.locator("div[class*='container__Container'] > div > ol[class*='results-styles'] > li > article[data-xds='Card']")
                print(cards.count())
                for i in range(cards.count()):
                    card = cards.nth(i)
                    href = card.locator("a").get_attribute("href")
                    if href:
                        job_urls.add("https://www.xing.com"+ href)
                page.close()
                page = browser.new_page()
            browser.close()
        return job_urls


if __name__=="__main__":
    xing_scraper = XingScraper()
    xing_scraper.run_scraper()
