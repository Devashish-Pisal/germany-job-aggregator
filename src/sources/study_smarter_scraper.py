from config.study_smarter_scraper_config import sss_config
from pprint import pprint
from playwright.sync_api import sync_playwright
import time

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


def extract_job_urls(query_url_list:list[str]) -> set[str]:
    job_urls = set()
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False, # Headless scraping is possible on study smarter platform
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



pprint(extract_job_urls(build_query_urls()))
