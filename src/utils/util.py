import hashlib


def generate_deduplication_key(title:str, company:str, location:str):
    normalized = f"{title.strip().lower()}|{company.strip().lower()}|{location.strip().lower()}"
    return hashlib.md5(normalized.encode()).hexdigest()