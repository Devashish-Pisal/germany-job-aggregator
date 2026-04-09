
config =  {

    # User query setting
    "country": ["germany"],                     # List of countries to search for job listings (case-insensitive)
    "city": ["mannheim"],                       # List of cities to search for job listings (case-insensitive)
    "distance": 40,                             # In kilometers
    "remote": False,                            # If set "True", then "city", "distance" fields will be ignored completely.
    "full_time": False,
    "part_time": False,
    "search_keywords": [                        # Synonymes of search terms (at the end results for all terms will be merged and duplicated will be removed) (case-insensitive)
        "Werkstudent IT Support",
        "Werkstudent IT",
        "Werkstudent Systemadministration",
        "Werkstudent IT Infrastruktur",
        "Werkstudent Software Tester",
        "Werkstudent QA",
        "Werkstudent Technical Support",
        "IT Support Mitarbeiter Werkstudent",
        "IT Helpdesk Werkstudent",
        "First Level Support Werkstudent",
        "Second Level Support Werkstudent",
        "IT Administrator Werkstudent",
        "IT Operations Werkstudent",
        "Application Support Werkstudent",
        "Software Tester Werkstudent",
        "QA Engineer Werkstudent",
        "Test Engineer Werkstudent",
        "Working Student IT Support",
        "Working Student System Administrator",
        "Working Student QA",
        "Technical Support Working Student",
    ],
    "output_filename": "jobs.csv",             # Currently only .csv output file formate is supported


    # Developer setting
    "use_adzuna_api": True,
    "use_arbeitsamt_api": True,
    "use_arbeitsnow_api": True,
    "use_findwork_api": True,                   # Developer focussed platform
    "max_pages": 1,
    "page_number": 1,
    "results_per_page": 250,
    "output_format": ".csv"                     # Currently only .csv output file format is supported
}
