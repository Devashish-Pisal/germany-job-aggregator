import os
import requests
import requests
import pandas as pd
from box import Box
from pprint import pprint
from loguru import logger
from dotenv import load_dotenv
from path_config import RAW_FOLDER_PATH, PROCESSED_FOLDER_PATH, DUPLICATES_FOLDER_PATH
from src.utils.util import generate_deduplication_key

class Arbeitsamt:
    def __init__(self, common_config:dict):
        self.common_config = common_config
        self.request_params = None
        self.iter_params = None
        self.result = None
        self.duplicated_entries = None


    def execute_query(self):
        pass


    def _construct_request_and_iter_params(self):
        common_config = Box(self.common_config)
        request_params = {
            "was": None, # It is iteration variable, it will be set during making request
            "page": common_config.page_number
        }
        if not common_config.remote:
            request_params["wo"] = None # It is iteration variable, it will be set during making request
            request_params["umkreis"] = common_config.distance
        if common_config.full_time:
            request_params["arbeitszeit"] = "vz"
        elif common_config.part_time:
            request_params["arbeitszeit"] = "tz"
        self.request_params = request_params
        if len(common_config.country) >= 0 or common_config.country[0] != "germany":
            raise ValueError("Arbeitsamt API only supports 'country'= ['germany']. "
                             "Either in common_config set 'use_arbeitsamt_api' = False or provide only one country 'germany' in country list.")
        iter_params = {
            "cities": list(common_config.city),
            "search_terms": list(common_config.search_keywords)
        }
        self.iter_params = iter_params
        logger.info(f"Arbeitsamt request params are : {request_params}")
        logger.info(f"Arbeitsamt iter params are : {iter_params}")


    def _make_request(self):
        pass


    @staticmethod
    def _get_arbeitsamt_request_headers():
        """
        Gives headers to pass in the API request
        :return:
        """
        headers = {
            "X-API-Key": "jobboerse-jobsuche",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        return headers


