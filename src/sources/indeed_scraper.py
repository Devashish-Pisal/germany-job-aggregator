import time
from pprint import pprint
from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright
from config.indeed_scraper_config import indeed_scraper_config


def build_query_urls() -> list[str]:
    urls = []
    location_radius_pairs = indeed_scraper_config["location_radius_pairs"]
    keywords_list = indeed_scraper_config["search_keywords"]
    job_age = indeed_scraper_config["job_age"]
    base_url = indeed_scraper_config["BASE_URL"]
    for k,v in location_radius_pairs.items():
        for kw in keywords_list:
            kw = quote_plus(kw.strip())
            k = quote_plus(k.strip())
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
            headless=False, # Headless scraping is not allowed on xing
        )
        page = browser.new_page()
        for url in query_url_list:
            print(url)
            page.goto(url)
            # page.pause()
            reject_cookies = page.locator("button[id='onetrust-reject-all-handler']")
            reject_cookies.click() # reject cookies
            page.wait_for_selector("div[class*='jobsearch-LeftPane']")
            empty_result = page.locator("div[class*='jobsearch-NoResult-messageContainer']").is_visible()
            if empty_result:
                print(f"No results found for query {url}")
                continue
            cards = page.locator("#mosaic-jobResults #mosaic-provider-jobcards ul > li[class*='css']  a[id*='job']") # > div[class*='vjs-highlight']
            print(cards.count())
            # page.pause()
            for i in range(cards.count()):
                card = cards.nth(i)
                href = card.get_attribute("href")
                if href:
                    if href.startswith("/rc/clk?"): # only allow valid hrefs
                        job_urls.add("https://de.indeed.com/viewjob?"+ href[8:len(href)]) # append href after removing "/rc/clk?"
                        # Example of href scraped from HTML: "/rc/clk?jk=7d79172975914a6c&bb=r6STzscjGymbQadnjPTxYUuqozf0DHAMtElUW1i-8QubawdLKL7PNk7qHQixZLOmLO8txAQbl6aGauzPwr5RmJ9qfLu45DUHWGh48l7WOW8mIynrK5nb77Q3GAeVHwaS&xkcb=SoCm67M3hFOv3FzNV50LbzkdCdPP&fccid=6a9687b53c8c4525&cmp=eiei-4-einzelhandel-gmbh&ti=IT+Manager&vjs=3"
        browser.close()
    return job_urls

output = extract_job_urls(build_query_urls())
print(len(output))
pprint(output)

