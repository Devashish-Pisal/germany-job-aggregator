import sys
import time
from pprint import pprint
from loguru import logger
from playwright.sync_api import sync_playwright
from config.stepstone_scraper_config import stepstone_scraper_config
from config.scraper_common_config import scraper_common_config
from src.utils.util import compute_embedding, get_emb_match_job_dict, compute_cosine_similarity



class StepstoneScraper:
    def __init__(self, embedding_model, keywords_embeddings):
        self.embedding_model = embedding_model
        self.keywords_embeddings = keywords_embeddings
        self.query_urls = None
        self.query_matched_emb_accepted_jobs = None
        self.query_matched_emb_rejected_jobs = None
        self.all_query_matched_job_urls = None
        self.all_query_matched_jobs = None # scrape job descriptions and construct list of JOB objects
        self.matching_jobs = None # Resume matching jobs in embedding space --> save these jobs into db immediately
        self.db_saved_jobs = None # Successfully saved jobs to the DB


    def run_scraper(self):
        # TODO: Surround following block with if to disable scraper
        self.query_urls = self.build_query_urls()
        logger.info(f"[Stepstone Scraper] Stepstone scraper built {len(self.query_urls)} query combinations")
        self.query_matched_emb_accepted_jobs, self.query_matched_emb_rejected_jobs = self.extract_job_urls(self.query_urls)
        logger.info(f"[Stepstone Scraper] Stepstone found total {len(self.query_matched_emb_accepted_jobs)} query matching accepted job urls and {len(self.query_matched_emb_rejected_jobs)} query matching rejected urls.")
        pprint(self.query_matched_emb_accepted_jobs)
        print(130*"=")
        pprint(self.query_matched_emb_rejected_jobs)


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



    def extract_job_urls(self, query_url_list:list[str]) -> tuple[list[dict], list[dict]]:
        accepted_job_urls = set()
        rejected_job_urls = set()
        accepted_jobs = []
        rejected_jobs = []

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
                        title = links.nth(i).locator("div").nth(2).inner_text()
                        threshold = scraper_common_config["embedding_match_config"]["threshold"]
                        if href and title:
                            href = "https://www.stepstone.de/"+ href
                            job_title_emb = compute_embedding(self.embedding_model, title)
                            max_sim = -sys.float_info.max
                            for query_emb in self.keywords_embeddings:
                                current_sim = compute_cosine_similarity(query_emb, job_title_emb)
                                if current_sim > max_sim:
                                    max_sim = current_sim
                            job = get_emb_match_job_dict(title, href, round(max_sim, 4), "stepstone")
                            if max_sim >= threshold and href not in accepted_job_urls:
                                accepted_job_urls.add(href)
                                accepted_jobs.append(job)
                            elif href not in rejected_job_urls:
                                rejected_job_urls.add(href)
                                rejected_jobs.append(job)
                                logger.warning(f"Rejecting {title} because max similarity score is {max_sim} | URL {href} | Threshold {scraper_common_config["embedding_match_config"]["threshold"]}")
                browser.close()
            except Exception as e:
                logger.warning(f"[Stepstone Scrapper] Caught exception {e} for url {url}")
        return accepted_jobs, rejected_jobs


if __name__=="__main__":
    pass
    # stepstone_scraper = StepstoneScraper()
    # stepstone_scraper.run_scraper()