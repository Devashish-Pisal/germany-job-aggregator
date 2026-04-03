
config =  {

    # User query setting
    "country": ["germany"],                     # List of countries to search for job listings
    "city": ["mannheim"],                       # List of cities to search for job listings
    "distance": 10,                             # In kilometers
    "remote": False,                            # If set "True", then "city", "distance" fields will be ignored completely.
    "full_time": False,
    "part_time": False,
    "search_keywords": [                        # Synonymes of search terms (at the end results for all terms will be merged and duplicated will be removed)
        "Python Engineer",
        "Python Entwickler"
    ],
    "page_number": 1,
    "results_per_page": 50,
    "max_pages": 5,
    "output_filename": "jobs.csv",             # Currently only .csv output file formate is supported



    # Developer setting
    "use_adzuna_api": True,
    "use_arbeitsamt_api": False,
    "use_arbeitsnow_api": False,
    "adzuna_app_id": None,                      # Injected during runtime (required in .env file, if "use_adzuna_api" is set to "True")
    "adzuna_api_key": None,                     # Injected during runtime (required in .env file, if "use_adzuna_api" is set to "True")
    "arbeitsamt_api_key": None,                 # Injected during runtime (currently not required)
    "arbeitsnow_api_key": None,                 # Injected during runtime (currently not required)
    "deduplication": {                          # Strategy to find the duplicated from the results
        "use_url": True,                        # If two job listings refer to the same reference url then it is duplicated listing
        "use_title_company_location": True,     # Create a key from "title & company & location" for each job listing and match that with existing job listings
    },
    "output_format": ".csv"                     # Currently only .csv output file format is supported
}
