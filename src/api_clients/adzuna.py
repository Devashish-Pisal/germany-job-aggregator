import os
import requests
import pandas as pd
from box import Box
from loguru import logger
from dotenv import load_dotenv
from path_config import RAW_FOLDER_PATH, PROCESSED_FOLDER_PATH, DUPLICATES_FOLDER_PATH
from src.utils.util import generate_deduplication_key


class Adzuna():
    def __init__(self, common_config:dict):
        self.common_config = common_config
        self.ADZUNA_APP_ID = None
        self.ADZUNA_APP_KEY = None
        self.request_params = None
        self.iter_params = None
        self.result = None
        self.duplicated_entries = None
        self._load_adzuna_secrets()


    def _load_adzuna_secrets(self):
        """
        Extract secret environment variables from .env file
        :return: None
        """
        if self.common_config["use_adzuna_api"]:
            logger.info("Using adzuna api!")
            self.ADZUNA_APP_ID = None
            self.ADZUNA_APP_KEY = None
            try:
                load_dotenv()
                self.ADZUNA_APP_ID = os.environ.get("ADZUNA_APP_ID")
                self.ADZUNA_APP_KEY = os.environ.get("ADZUNA_API_KEY")
                logger.info("Adzuna secret credentials loaded successfully.")
            except Exception:
                logger.exception("Unable to load Adzuna secret credentials!")


    def execute_query(self):
        """
        Combines all methods from the class together and executes all of them in clean pipeline manner.
        :return: None
        """
        self._construct_request_and_iter_params()
        self._make_requests()
        self._save_csv_files()


    def _construct_request_and_iter_params(self):
        """
        Creates request parameters to send with requests and creates iteration parameters to inject in request parameters one by one.
        :return: None
        """
        common_config = Box(self.common_config)
        request_params = {
            "app_id": self.ADZUNA_APP_ID,
            "app_key": self.ADZUNA_APP_KEY,
            "results_per_page": common_config.results_per_page,
            "what": None, # It is iteration variable, it will be set during making request
        }
        if not common_config.remote:
            request_params["where"] = None # It is iteration variable, it will be set during making request
            request_params["distance"] = common_config.distance
        if common_config.full_time:
            request_params["full_time"] = "1"
        if common_config.part_time:
            request_params["part_time"] = "1"
        self.request_params = request_params
        iter_params = {
            "countries" : [self._get_country_code_mappings()[country] for country in common_config.country],
            "cities": list(common_config.city),
            "search_terms": list(common_config.search_keywords),
        }
        self.iter_params = iter_params
        logger.info(f"Adzuna iter params are : {iter_params}")


    def _make_requests(self):
        """
        Make multiple requests to adzuna by iterating over self.iter_params
        :return: None
        """
        countries = self.iter_params["countries"]
        cities = self.iter_params["cities"]
        search_terms = self.iter_params["search_terms"]
        request_params = self.request_params
        adzuna_result = pd.DataFrame({
            "area": [],
            "company": [],
            "title": [],
            "redirect_url": [],
            "deduplication_key": []
        })
        duplicated_entries = pd.DataFrame({
            "area": [],
            "company": [],
            "title": [],
            "redirect_url": [],
            "deduplication_key": []
        })
        for country in countries:
            for city in cities:
                for term in search_terms:
                    request_url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{self.common_config['page_number']}"
                    if not self.common_config["remote"]:
                        request_params["where"] = city
                        request_params["what"] = term
                        response = requests.get(url=request_url, params=request_params, headers=self._get_adzuna_request_headers())
                        if response.status_code != 200:
                            logger.error(f"Status: {response.status_code}")
                            logger.error(f"Response: {response.text}")
                            logger.error(f"URL: {response.url}")
                            logger.error(f"Params: {request_params}")
                        else:
                            data = response.json()
                            output = data["results"]
                            rows = []
                            for dictionary in output:
                                title = dictionary["title"].strip().lower()
                                company = dictionary["company"]["display_name"].strip().lower()
                                location = dictionary["location"]["area"][-1]
                                dedup_key = generate_deduplication_key(title, company, location)
                                rows.append({
                                    "area": ", ".join([item.strip().lower() for item in dictionary["location"]["area"]]),
                                    "company": company,
                                    "title": title,
                                    "redirect_url": dictionary["redirect_url"],
                                    "deduplication_key": dedup_key
                                })
                            result_1 = pd.DataFrame(rows)
                            # Deduplicate
                            df_to_add = result_1[~result_1["redirect_url"].isin(adzuna_result["redirect_url"])]
                            df_to_add = df_to_add[~df_to_add["deduplication_key"].isin(adzuna_result["deduplication_key"])]
                            # Capture duplicates before adding to main result
                            duplicated_entry_1 = result_1[result_1["redirect_url"].isin(adzuna_result["redirect_url"])]
                            duplicated_entry_2 = result_1[result_1["deduplication_key"].isin(adzuna_result["deduplication_key"])]
                            current_duplicates = pd.concat([duplicated_entry_1, duplicated_entry_2],ignore_index=True)
                            # If self.duplicated_entries already exists (non-empty), filter out overlapping duplicates
                            if not duplicated_entries.empty:
                                current_duplicates = current_duplicates[~current_duplicates["redirect_url"].isin(duplicated_entries["redirect_url"])]
                                current_duplicates = current_duplicates[~current_duplicates["deduplication_key"].isin(duplicated_entries["deduplication_key"])]
                            # Add the filtered duplicates to the class-level accumulator
                            duplicated_entries = pd.concat([duplicated_entries, current_duplicates],ignore_index=True)
                            # Add unique entries
                            adzuna_result = pd.concat([adzuna_result, df_to_add], ignore_index=True)
                    else:
                        logger.error("Remote job search for adzuna is not implemented yet!")
        self.result = adzuna_result
        self.duplicated_entries = duplicated_entries
        logger.info(f"Total received unique results are {len(self.result)}.")
        logger.info(f"Total found duplicated entries are {len(self.duplicated_entries)}")


    def _save_csv_files(self):
        """
        Saves raw CSV files of adzuna unique job postings in folder data/raw and adzuna duplicated job postings in folder data/duplicated
        :return: None
        """
        file_path = os.path.join(RAW_FOLDER_PATH,"adzuna_" + self.common_config["output_filename"])
        self.result.to_csv(file_path, encoding="utf-8", index=False)
        logger.info(f"Raw output data is stored at location {file_path}")

        duplicates_file_path = os.path.join(DUPLICATES_FOLDER_PATH, "adzuna_duplicates.csv")
        self.duplicated_entries.to_csv(duplicates_file_path, encoding="utf-8", index=False)
        logger.info(f"Adzuna duplicate job entries stored at location {duplicates_file_path}")


    @staticmethod
    def _get_adzuna_request_headers():
        """
        Gives headers to pass in the API request
        :return:
        """
        headers = {
            "Accept": "application/json"
        }
        return headers


    @staticmethod
    def _get_country_code_mappings():
        """
        Maps country names with their ISO 8601 country codes
        :return: Mapping of country names with their ISO 8601 country codes
        """
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
