from config.study_smarter_scraper_config import sss_config
from pprint import pprint
from playwright.sync_api import sync_playwright
import time


class StudySmarterScraper:
    def __init__(self):
        self.query_urls = None
        self.all_query_matched_job_urls = None
        self.all_query_matched_jobs = None  # scrape job descriptions and construct list of JOB objects
        self.matching_jobs = None  # Resume matching jobs in embedding space --> save these jobs into db immediately
        self.db_saved_jobs = None  # Successfully saved jobs to the DB


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
        location_radius_pairs = sss_config["location_radius_pairs"]
        keywords_list = sss_config["search_keywords"]
        job_age = sss_config["job_age"]
        base_url = sss_config["BASE_URL"]
        for k,v in location_radius_pairs.items():
            for kw in keywords_list:
                kw = kw.strip().lower().replace(" ", "+")
                k = k.strip().replace(" ", "+")
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
                headless=sss_config["use_headless_mode"], # Headless scraping is possible on study smarter platform
            )
            page = browser.new_page()
            for url in query_url_list:
                page.goto(url)
                page.wait_for_selector(".c-job-cards")
                cards = page.locator(".c-job-card")
                print(cards.count())
                for i in range(cards.count()):
                    card = cards.nth(i)
                    href = card.locator("a").get_attribute("href")
                    if href:
                        job_urls.add(href)
                page.close()
                page = browser.new_page()
            browser.close()
        return job_urls


if __name__=="__main__":
    ss_scraper = StudySmarterScraper()
    ss_scraper.run_scraper()
