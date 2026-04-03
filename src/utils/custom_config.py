from box import Box
from config.common_config import config



def get_country_code_mappings():
    country_code_mapping = {
        "united kingdom": "gb",
        "united states": "us",
        "austria": "at",
        "australia": "au",
        "belgium": "be",
        "brazil": "br",
        "canada": "ca",
        "switzerland": "ch",
        "germany": "de",
        "spain": "es",
        "france": "fr",
        "india": "in",
        "italy": "it",
        "mexico": "mx",
        "netherlands": "nl",
        "new zealand": "nz",
        "poland": "pl",
        "singapore": "sg",
        "south africa": "za",
    }
    return country_code_mapping



def create_adzuna_params(config:dict, app_id:str, app_key: str) -> dict:
    # https://developer.adzuna.com/activedocs#/default/search
    config = Box(config)
    country_code_mappings = get_country_code_mappings()
    adzuna_params = {
        "country": [country_code_mappings[country.strip().lower()] for country in config.country],
        "page": config.page_number,
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": config.results_per_page,
        "what": [kw.strip().lower() for kw in config.search_keywords],
        "distance": config.distance,
    }
    if not config.remote:
        adzuna_params["where"] = [city.strip().lower() for city in config.city]
        adzuna_params["distance"] = config.distance
    if config.full_time:
        adzuna_params["full_time"] = "1"
    if config.part_time:
        adzuna_params["part_time"] = "1"
    return adzuna_params




