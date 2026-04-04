from box import Box
from config.common_config import config
from loguru import logger


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



def check_prerequisite(client:str, config:Box):
    client = client.strip().lower()
    match client:
        case "adzuna":
            if config.country is None or len(config.country) == 0:
                logger.error("'country' attribute is required in order to search on adzuna.")
                exit()
            if config.page_number is None or not isinstance(config.page_number, int) or config.page_number <= 0:
                logger.error("'page_number' attribute is required in oder to search on adzuna. It must be integer and greater than 0.")
                exit()
        case _:
            logger.error(f"Prerequisite check for '{client}' is not implemented yet!")
            exit()




def create_adzuna_params(config:dict, app_id:str, app_key: str) -> dict:
    # https://developer.adzuna.com/activedocs#/default/search
    config = Box(config)
    check_prerequisite( "adzuna", config)
    if not app_id or not app_key:
        logger.error("'app-id' and 'app_key' must be provided to construct adzuna request parameters and it must not be empty string.")
    adzuna_params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": config.results_per_page,
        "what": [kw.strip().lower() for kw in config.search_keywords],
    }
    if not config.remote:
        adzuna_params["where"] = [city.strip().lower() for city in config.city]
        adzuna_params["distance"] = config.distance
    if config.full_time:
        adzuna_params["full_time"] = "1"
    if config.part_time:
        adzuna_params["part_time"] = "1"
    return adzuna_params



