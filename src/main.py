from loguru import logger

from config.indeed_scraper_config import indeed_scraper_config
from path_config import LOGS_FOLDER_PATH
from datetime import datetime

from src.sources.arbeitsamt import Arbeitsamt
from src.sources.findwork import FindWork
from src.sources.study_smarter_scraper import StudySmarterScraper
from src.utils.validate_config import  ValidateConfig
from config.common_config import config
from src.sources.adzuna import Adzuna

# TODO: CREATE DATA FOLDER AND SUBFOLDERS (IF NOT EXISTS)

'''
cfg = None
try:
    cfg = ValidateConfig(**config)
    cfg = dict(cfg)
except Exception:
    logger.exception("Config validation failed")
    exit(1)

adzuna = Adzuna(cfg)
adzuna.execute_query()



arbeitsamt = Arbeitsamt(cfg)
arbeitsamt.execute_query()
findwork = FindWork(cfg)
findwork.execute_query()
exit()


# Log file setup
log_file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_job-aggregator-run.log"
log_file_path = str(LOGS_FOLDER_PATH / log_file_name)
logger.add(log_file_path, rotation="10 MB", level="INFO")
'''
import time
from pprint import pprint
from config.scraper_common_config import scraper_common_config
from sources.indeed_scraper import IndeedScraper
from sources.xing_scraper import XingScraper
from sources.stepstone_scraper import StepstoneScraper
from sources.study_smarter_scraper import StudySmarterScraper
from sentence_transformers import SentenceTransformer
from src.utils.util import compute_search_keywords_embeddings


start = time.time()
embedding_model = SentenceTransformer(scraper_common_config["embedding_match_config"]["sentence_embedding_model"])
logger.info("Model loaded!")
kw_embeddings = compute_search_keywords_embeddings(embedding_model, scraper_common_config["search_keywords"])

# indeed_result = []
# xing_result = []
stepstone_result = []
# study_smarter_result = []

# indeed_scraper = IndeedScraper()
# xing_scraper = XingScraper()
stepstone_scraper = StepstoneScraper(embedding_model, kw_embeddings)
# ss_scraper = StudySmarterScraper(embedding_model=embedding_model, keyword_embeddings=kw_embeddings)

# indeed_scraper.run_scraper()
# xing_scraper.run_scraper()
stepstone_scraper.run_scraper()
# ss_scraper.run_scraper()

# indeed_result.extend(indeed_scraper.all_query_matched_job_urls)
# xing_result.extend(xing_scraper.all_query_matched_job_urls)
stepstone_result.extend(stepstone_scraper.all_query_matched_job_urls)
# study_smarter_result.extend(ss_scraper.query_matched_emb_accepted_jobs)

end = time.time()


print("="*130)
print(f"FINAL AGGREGATED RESULT - {len(stepstone_result)} items")
for item in stepstone_result:
    pprint(item)
print("="*130)
print(f"Scraping took {((end-start)/60):.2f} minutes")
print("="*130)

print(f"REJECTED ITEMS - {len(stepstone_scraper.query_matched_emb_rejected_jobs)} items")
pprint(stepstone_scraper.query_matched_emb_rejected_jobs)
print("="*130)