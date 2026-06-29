indeed_scraper_config = {
    "use_headless_mode": False,
    "BASE_URL": "https://de.indeed.com/jobs?q={keywords}&l={location}&fromage={job_age}&radius={radius}",
    "location_radius_pairs": {
        # Allowed radius lengths for indeed are : 0, 5, 10, 15, 25, 35, 40, 50, 100
        "Mannheim, Baden-Württemberg": 25,
        # "Frankfurt am Main": 20,
    },
    "job_age": 7,  # Allowed number of days old job for indeed is (1, 3, 7, 14)
    "search_keywords": [
        "Werkstudent KI",
        "Werkstudent Automatisierung",
    ],
}