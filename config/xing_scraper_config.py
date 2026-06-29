xing_scraper_config = {
    "use_headless_mode": False,
    "BASE_URL": "https://www.xing.com/jobs/search/ki?keywords={keywords}&location={location}&radius={radius}&sincePeriod={job_age}",
    "location_radius_pairs" : {
        # Allowed radius lengths for xing are : 0, 10, 20, 50, 70, 100, 200
        "Mannheim": 0,
        # "Frankfurt am Main": 20,
    },
    "job_age": "LAST_WEEK", # Allowed number of days old job for xing is : LAST_24_HOURS, LAST_WEEK, LAST_MONTH
    "search_keywords": [
        # Werkstudent KI,
        # "Werkstudent Automatisierung",
        "Werkstudent"
    ],
}
