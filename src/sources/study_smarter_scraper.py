from config.study_smarter_scraper_config import sss_config
from pprint import pprint
from playwright.sync_api import sync_playwright
import time
from loguru import logger
from config.scraper_common_config import scraper_common_config
from src.utils.util import compute_embedding, compute_cosine_similarity



class StudySmarterScraper:
    def __init__(self, embedding_model, keyword_embeddings):
        self.embedding_model = embedding_model
        self.keywords_embeddings = keyword_embeddings
        self.query_urls = None
        self.query_matched_emb_accepted_urls = None
        self.query_matched_emb_rejected_urls = None
        self.all_query_matched_jobs = None  # scrape job descriptions and construct list of JOB objects
        self.matching_jobs = None  # Resume matching jobs in embedding space --> save these jobs into db immediately
        self.db_saved_jobs = None  # Successfully saved jobs to the DB



    def run_scraper(self):
        # TODO: Surround following block with if to disable scraper
        self.query_urls = self.build_query_urls()
        logger.info(f"[Studysmarter Scraper] Studysmarter scraper built {len(self.query_urls)} query combinations")
        self.query_matched_emb_accepted_urls, self.query_matched_emb_rejected_urls = self.extract_job_urls(self.query_urls)
        logger.info(f"[Studysmarter Scraper] Studysmarter found total {len(self.query_matched_emb_accepted_urls)} query matching accepted job urls and {len(self.query_matched_emb_rejected_urls)} query matching rejected urls.")



    @staticmethod
    def build_query_urls() -> list[str]:
        urls = []
        location_radius_pairs = sss_config["location_radius_pairs"]
        keywords_list = scraper_common_config["search_keywords"]
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


    def extract_job_urls(self, query_url_list:list[str]) -> tuple[set[str], set[str]]:
        accepted_job_urls = set()
        rejected_job_urls = set()
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=sss_config["use_headless_mode"], # Headless scraping is possible on study smarter platform
            )
            page = browser.new_page()
            try:
                for url in query_url_list:
                    page.goto(url, wait_until="domcontentloaded")
                    page.wait_for_selector("div[class*='results__jobs']")
                    card_visible = page.locator("div[class='c-job-cards']").is_visible()
                    if not card_visible:
                        logger.info(f"[Studysmarter Scraper] No matching job posting results found for query {url}")
                        continue
                    cards = page.locator("div[class='c-job-card ']")
                    for i in range(cards.count()):
                        card = cards.nth(i)
                        title = card.locator("div[class*='c-job-card'] h4[class*='c-job-card__title']").inner_text()
                        href = card.locator("a").get_attribute("href")
                        threshold = scraper_common_config["embedding_match_config"]["threshold"]
                        if title and href:
                            job_title_emb = compute_embedding(self.embedding_model, title)
                            matched = False
                            for query_emb in self.keywords_embeddings:
                                sim = compute_cosine_similarity(query_emb, job_title_emb)
                                if sim >= threshold:
                                    accepted_job_urls.add(href)
                                    matched = True
                                    break
                            if not matched:
                                rejected_job_urls.add(href)
                                logger.warning(f"Rejecting {title} because last similarity score is {sim} | URL {href} | Threshold {scraper_common_config["embedding_match_config"]["threshold"]}")
                browser.close()
            except Exception as e:
                logger.warning(f"[Studysmarter Scrapper] Caught exception {e} for url {url}")
        return accepted_job_urls, rejected_job_urls


if __name__=="__main__":
    ss_scraper = StudySmarterScraper()
    ss_scraper.run_scraper()
