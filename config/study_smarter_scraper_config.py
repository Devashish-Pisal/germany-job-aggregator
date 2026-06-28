sss_config = {
    "use_headless_mode": False,
    "BASE_URL": "https://talents.studysmarter.de/jobs/?keyword={keywords}&page_number=1&job_listing_type=&job_listing_category=&job_listing_tag=&job_listing_company_size=&job_listing_industry=&job_listing_seniority_level=&is_remote_position=&city={location}&radius={radius}&isResetClicked=false&easy_apply=&salary_min=&salary_max=&job_age={job_age}&premium_only=",
    "location_radius_pairs" : {
        # Allowed radius lengths for study smarter are : 1, 10, 20, 30, 40, 50
        "Mannheim": 50,
        "Frankfurt am Main": 20,
    },
    "job_age": 1, # Allowed number of days old job for study smarter is (1, 7, 30)
    "search_keywords": [
        "Werkstudent KI",
        "Werkstudent Automatisierung",
    ],
}
