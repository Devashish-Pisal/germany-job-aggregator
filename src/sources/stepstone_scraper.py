from pprint import pprint
from loguru import logger
from playwright.sync_api import sync_playwright
from config.stepstone_scraper_config import stepstone_scraper_config
from config.scraper_common_config import scraper_common_config



class StepstoneScraper:
    def __init__(self):
        self.query_urls = None
        self.all_query_matched_job_urls = None
        self.all_query_matched_jobs = None # scrape job descriptions and construct list of JOB objects
        self.matching_jobs = None # Resume matching jobs in embedding space --> save these jobs into db immediately
        self.db_saved_jobs = None # Successfully saved jobs to the DB


    def run_scraper(self):
        # TODO: Surround following block with if to disable scraper
        self.query_urls = self.build_query_urls()
        logger.info(f"[Stepstone Scraper] Stepstone scraper built {len(self.query_urls)} query combinations")
        self.all_query_matched_job_urls = self.extract_job_urls(self.query_urls)
        logger.info(f"[Stepstone Scraper] Stepstone found total {len(self.all_query_matched_job_urls)} query matching job urls")



    @staticmethod
    def build_query_urls() -> list[str]:
        urls = []
        location_radius_pairs = stepstone_scraper_config["location_radius_pairs"]
        keywords_list = scraper_common_config["search_keywords"]
        job_age = stepstone_scraper_config["job_age"]
        base_url = stepstone_scraper_config["BASE_URL"]
        for k,v in location_radius_pairs.items():
            for kw in keywords_list:
                kw = kw.strip().lower().replace(" ", "-")
                k = k.strip().lower().replace(" ", "-")
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
                headless=stepstone_scraper_config["use_headless_mode"], # Headless scraping is not allowed on stepstone
            )
            page = browser.new_page()
            try:
                for url in query_url_list:
                    page.goto(url)
                    page.wait_for_selector("div[class*='res-'][data-genesis-element='BASE']")
                    # TODO: add accept cookies logic
                    valid_hits = page.locator("[data-resultlist-offers-numbers]")
                    number_of_valid_hits_displayed = int(valid_hits.get_attribute("data-resultlist-offers-main-displayed")) # only collect urls of valid jobs (not recommendations) from page 1
                    if number_of_valid_hits_displayed == 0:
                        logger.info(f"[Stepstone Scraper] No matching job posting results found for query {url}")
                        continue
                    links = page.locator("a[href*='/stellenangebote']")
                    for i in range(number_of_valid_hits_displayed):
                        href = links.nth(i).get_attribute("href")
                        if href:
                            job_urls.add("https://www.stepstone.de/"+ href)
                browser.close()
            except Exception as e:
                logger.warning(f"[Stepstone Scrapper] Caught exception {e} for url {url}")
        return job_urls


if __name__=="__main__":
    stepstone_scraper = StepstoneScraper()
    stepstone_scraper.run_scraper()