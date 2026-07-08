import hashlib
import re
import numpy as np

def generate_deduplication_key(title:str, company:str, location:str):
    normalized = f"{title.strip().lower()}|{company.strip().lower()}|{location.strip().lower()}"
    return hashlib.md5(normalized.encode()).hexdigest()


NOISE_WORDS = [
    # employment type
    "werkstudent",
    "working student",
    "praktikum",
    "intern",
    "hiwi",
    "student",
    "studentenjob",
    "research assistant",
    "wissenschaftliche hilfskraft",
    # gender / legal
    "m/w/d",
    "w/m/d",
    "m/f/d",
    "f/m/x",
    "m/w/x",
    "all genders",
    "gn",
    # contract / meta
    "full time",
    "part time",
    "teilzeit",
    "vollzeit",
    "remote",
    "hybrid",
    "onsite",
    "home office",
    "befristet",
    "unbefristet",
    # job board noise
    "job id",
    "job-id",
    "ref",
]


def clean_search_keywords_and_job_title(text: str) -> str:
    text = text.lower()
    for w in NOISE_WORDS:
        text = text.replace(w, " ")
    # remove special characters like (m/w/d)
    text = re.sub(r"\(.*?m.*?w.*?d.*?\)", " ", text)
    # remove leftover brackets and symbols
    text = re.sub(r"[\(\)\|\-_/,:;]", " ", text)
    # normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def compute_search_keywords_embeddings(model, keywords:list[str]):
    output =[]
    for kw in keywords:
        emb = compute_embedding(model, kw)
        output.append(emb)
    return np.array(output)


def compute_embedding(model, job_title:str):
    cleaned = clean_search_keywords_and_job_title(job_title)
    emb = model.encode(cleaned, normalize_embeddings=True)
    return emb


def compute_cosine_similarity(query_emb, job_embs):
    # cosine similarity = dot product (because normalized)
    return job_embs @ query_emb