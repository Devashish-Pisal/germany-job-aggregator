import json
import os
import re
import requests
import pandas as pd
from box import Box
from pprint import pprint
from loguru import logger
from dotenv import load_dotenv
from path_config import RAW_FOLDER_PATH, PROCESSED_FOLDER_PATH, DUPLICATES_FOLDER_PATH
from src.utils.util import generate_deduplication_key


"""
api_key= "083dced6-f247-476d-8429-0b4685defe2b"
url  = f"https://jooble.org/api/{api_key}"
params = {
    "keywords": "python developer",
    "location": "mannheim",
}
headers = {"Content-type": "application/json"}
response = requests.post(url, params=params, headers=headers)
print(response.status_code)
pprint(response.text)
print(response.url)
exit()
"""

import http.client

host = 'jooble.org'
key = '083dced6-f247-476d-8429-0b4685defe2b'

connection = http.client.HTTPConnection(host)
#request headers
headers = {"Content-type": "application/json"}
#json query
body = '{ "keywords": "python developer", "location": "germany"}'
connection.request('POST','/api/' + key, body, headers)
response = connection.getresponse()
print(response.status, response.reason)
data = json.loads(response.read().decode("utf-8"))
print(data)
pprint(data["jobs"])
exit()

