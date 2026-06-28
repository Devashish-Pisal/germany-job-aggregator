from pprint import pprint
from playwright.sync_api import sync_playwright
from config.stepstone_scraper_config import stepstone_scraper_config


def build_query_urls() -> list[str]:
    urls = []
    location_radius_pairs = stepstone_scraper_config["location_radius_pairs"]
    keywords_list = stepstone_scraper_config["search_keywords"]
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


def extract_job_urls(query_url_list:list[str]) -> set[str]:
    job_urls = set()
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False, # Headless scraping is not allowed on stepstone
        )
        page = browser.new_page()
        for url in query_url_list:
            print(url)
            page.goto(url)
            page.wait_for_selector("div[class*='res-'][data-genesis-element='BASE']")
            valid_hits = page.locator("[data-resultlist-offers-numbers]")
            number_of_valid_hits_displayed = int(valid_hits.get_attribute("data-resultlist-offers-main-displayed")) # only collect urls of valid jobs (not recommendations) from page 1
            links = page.locator("a[href*='/stellenangebote']")
            for i in range(number_of_valid_hits_displayed):
                href = links.nth(i).get_attribute("href")
                if href:
                    job_urls.add("https://www.stepstone.de/"+ href)
            page.close()
            page = browser.new_page()
        browser.close()
    return job_urls


output = extract_job_urls(build_query_urls())
pprint(output)
print(len(output))
