from typing import List, Literal
from box import Box
from loguru import logger
from pydantic import BaseModel, Field, field_validator


class Deduplication(BaseModel):
    use_url: bool
    use_title_company_location: bool


class ValidateConfig(BaseModel):
    country:List[str]
    city:List[str]
    distance: int = Field(gt=0)
    remote: bool
    full_time: bool
    part_time: bool
    search_keywords: List[str]
    page_number: int = Field(gt=0)
    results_per_page: int = Field(gt=0)
    max_pages: int = Field(gt=0)
    output_filename: str = Field(pattern=r"\.csv$")
    use_adzuna_api: bool
    use_arbeitsamt_api: bool
    use_arbeitsnow_api: bool
    deduplication: Deduplication
    output_format: Literal[".csv"]


    @field_validator("country", "city", "search_keywords", mode="before")
    @classmethod
    def lower_list_items(cls, v):
        if isinstance(v, str):
            return [v.strip().lower()]
        if isinstance(v, list):
            return [v_item.strip().lower() if isinstance(v_item, str) else v_item for v_item in v]
        return v


    def validate_adzuna_api_prerequisite(self):
        pass

    def validate_arbeitsamt_api_prerequisite(self):
        pass

    def validate_arbeitsnow_api_prerequisite(self):
        pass


class ConfigUtil:
    def __init__(self, common_config:dict):
        self.common_config = common_config

    def validate_common_config(self):
        pass

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



