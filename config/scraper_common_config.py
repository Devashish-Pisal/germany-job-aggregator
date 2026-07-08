scraper_common_config = {
    "scraping_browser_profile_path": "E:\(_Coding_Data_)\Selenium_Chrome_Profiles\job_listing_data_scrapping_profile", # currently only used by indeed scraper
    "keywords_job_title_must_include": [], # Job title will always include at least one keyword from the list (OR operation)
    "keywords_job_title_must_exclude": [],  # Job title will never include any keyword from the list (AND operation)
    "embedding_match_config": {
        "sentence_embedding_model": "BAAI/bge-m3", # model is used to compare the 'query keyword' and 'job title' match and to filter false positives
        "threshold": 0.75, # to filter non-relevant (or less relevant) job listings
    },

"search_keywords" :  [
        # German
        "Werkstudent KI",
        "Werkstudent Künstliche Intelligenz",
        "Werkstudent Generative KI",
        "Werkstudent Generative AI",
        "Werkstudent LLM",
        "Werkstudent AI",
        "Werkstudent AI Engineer",
        "Werkstudent KI Entwicklung",
        "Werkstudent AI Entwicklung",
        "Werkstudent KI Softwareentwicklung",
        "Werkstudent Machine Learning",
        "Werkstudent Maschinelles Lernen",
        "Werkstudent NLP",
        "Werkstudent Prompt Engineering",
        "Werkstudent AI Software Engineer",
        "Werkstudent Applied AI",
        "Werkstudent AI Solutions",
        # English
        "Working Student AI",
        "Working Student AI Engineer",
        "Working Student Artificial Intelligence",
        "Working Student Machine Learning",
        "Working Student ML Engineer",
        "Working Student Generative AI",
        "Working Student LLM",
        "Working Student NLP",
        "Working Student Applied AI",
        "Working Student AI Developer",
        "Working Student AI Software Engineer",
        "Working Student AI Solutions",
        "Working Student AI Applications",
        "Working Student Prompt Engineering",
        # Internship variants
        "Praktikum KI",
        "Praktikum Künstliche Intelligenz",
        "Praktikum Machine Learning",
        "Praktikum AI",
        "Intern AI",
        "Intern Machine Learning",
        "Intern LLM",
        "Intern Generative AI",
    ],
}












"""
ALL KEYWORDS: 


    "search_keywords" :  [
    # search keywords will be dynamically normalized/adjusted by every scraper at runtime (keep default format, every words first letter capitalized, e.g Working Student Python)
        # ==========================================================
        # 1. AUTOMATION / DIGITALIZATION (Highest Priority)
        # ==========================================================
        # German
        "Werkstudent Automatisierung",
        "Werkstudent Prozessautomatisierung",
        "Werkstudent Softwareautomatisierung",
        "Werkstudent Digitalisierung",
        "Werkstudent Digitale Transformation",
        "Werkstudent Prozessdigitalisierung",
        "Werkstudent Intelligent Automation",
        "Werkstudent Business Automation",
        "Werkstudent KI Automatisierung",
        "Werkstudent Automatisierungstechnik",
        "Werkstudent Digitalisierungsprojekte",
        "Werkstudent Digitale Lösungen",
        "Werkstudent Innovation",
        "Werkstudent Digital Innovation",
        # English
        "Working Student Automation",
        "Working Student Process Automation",
        "Working Student Intelligent Automation",
        "Working Student Business Automation",
        "Working Student Digital Transformation",
        "Working Student Digitalization",
        "Working Student Digital Solutions",
        "Working Student Automation Engineer",
        "Working Student Automation Developer",
        "Working Student Software Automation",
        "Working Student Innovation",
        "Working Student Digital Innovation",
        # Internship variants
        "Praktikum Automatisierung",
        "Praktikum Digitalisierung",
        "Praktikum Digitale Transformation",
        "Intern Automation",
        "Intern Digital Transformation",
        # ==========================================================
        # 2. AI / LLM / MACHINE LEARNING (Second Highest Priority)
        # ==========================================================
        # German
        "Werkstudent KI",
        "Werkstudent Künstliche Intelligenz",
        "Werkstudent Generative KI",
        "Werkstudent Generative AI",
        "Werkstudent LLM",
        "Werkstudent AI",
        "Werkstudent AI Engineer",
        "Werkstudent KI Entwicklung",
        "Werkstudent AI Entwicklung",
        "Werkstudent KI Softwareentwicklung",
        "Werkstudent Machine Learning",
        "Werkstudent Maschinelles Lernen",
        "Werkstudent NLP",
        "Werkstudent Prompt Engineering",
        "Werkstudent AI Software Engineer",
        "Werkstudent Applied AI",
        "Werkstudent AI Solutions",
        # English
        "Working Student AI",
        "Working Student AI Engineer",
        "Working Student Artificial Intelligence",
        "Working Student Machine Learning",
        "Working Student ML Engineer",
        "Working Student Generative AI",
        "Working Student LLM",
        "Working Student NLP",
        "Working Student Applied AI",
        "Working Student AI Developer",
        "Working Student AI Software Engineer",
        "Working Student AI Solutions",
        "Working Student AI Applications",
        "Working Student Prompt Engineering",
        # Internship variants
        "Praktikum KI",
        "Praktikum Künstliche Intelligenz",
        "Praktikum Machine Learning",
        "Praktikum AI",
        "Intern AI",
        "Intern Machine Learning",
        "Intern LLM",
        "Intern Generative AI",
        # ==========================================================
        # 3. PYTHON / BACKEND (Third Highest Priority)
        # ==========================================================
        # German
        "Werkstudent Python",
        "Werkstudent Python Entwickler",
        "Werkstudent Python Entwicklung",
        "Werkstudent Python Backend",
        "Werkstudent Backend",
        "Werkstudent Backend Entwickler",
        "Werkstudent Backend Entwicklung",
        "Werkstudent Softwareentwickler Python",
        "Werkstudent Softwareentwicklung Python",
        "Werkstudent API Entwicklung",
        "Werkstudent FastAPI",
        "Werkstudent REST API",
        "Werkstudent Webentwicklung Python",
        # English
        "Working Student Python",
        "Working Student Python Developer",
        "Working Student Python Backend",
        "Working Student Backend Developer",
        "Working Student Backend Engineer",
        "Working Student Software Engineer Python",
        "Working Student Software Developer Python",
        "Working Student API Developer",
        "Working Student FastAPI",
        "Working Student REST API",
        # Internship variants
        "Praktikum Python",
        "Praktikum Backend",
        "Intern Python Developer",
        "Intern Backend Developer",
        # ==========================================================
        # 4. RESEARCH / COMPUTER VISION (Lower Priority)
        # ==========================================================
        # German
        "Werkstudent Computer Vision",
        "Werkstudent Bildverarbeitung",
        "Werkstudent Deep Learning",
        "Werkstudent OCR",
        "Werkstudent Dokumentenanalyse",
        "Werkstudent Vision AI",
        "Werkstudent Multimodale KI",
        "Werkstudent AI Research",
        "HiWi KI",
        "HiWi Machine Learning",
        "HiWi Computer Vision",
        "Wissenschaftliche Hilfskraft KI",
        # English
        "Working Student Computer Vision",
        "Working Student Vision AI",
        "Working Student Deep Learning",
        "Working Student OCR",
        "Working Student Image Processing",
        "Working Student Document AI",
        "Working Student AI Research",
        "Working Student Applied Research",
        "Research Assistant AI",
        "Student Research Assistant AI",
        # Internship variants
        "Praktikum Computer Vision",
        "Intern Computer Vision",
        "Intern Deep Learning",
        # ==========================================================
        # 5. DATA ENGINEERING / DATA SCIENCE (Lowest Priority)
        # ==========================================================
        # German
        "Werkstudent Data Engineer",
        "Werkstudent Data Science",
        "Werkstudent Datenanalyse",
        # English
        "Working Student Data Engineer",
        "Working Student Data Science",
        "Working Student Data Analytics",
        # Internship variants
        "Intern Data Science",
    ], 
    
"""