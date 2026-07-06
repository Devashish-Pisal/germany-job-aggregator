indeed_scraper_config = {
    "use_headless_mode": False,
    "delay_between_consecutive_queries": 2, # seconds
    "BASE_URL": "https://de.indeed.com/jobs?q={keywords}&l={location}&fromage={job_age}&radius={radius}",
    "location_radius_pairs": {
        # Allowed radius lengths for indeed are : 0, 5, 10, 15, 25, 35, 40, 50, 100
        "Mannheim, Baden-Württemberg": 25,
        "Heidelberg, Baden-Württemberg": 25,
        "Ludwigshafen am Rhein, Rheinland-Pfalz": 25,
        "Walldorf, Baden-Württemberg": 25,
        "Karlsruhe, Baden-Württemberg": 25,
        "Kaiserslautern, Rheinland-Pfalz": 25,
        "Darmstadt, Hessen": 25,
        "Frankfurt am Main, Hessen": 25,
        "Stuttgart, Baden-Württemberg": 25,
    },
    "job_age": 7,  # Allowed number of days old job for indeed is (1, 3, 7, 14)
}