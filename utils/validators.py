import re
from typing import Optional


def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_linkedin_url(url: str) -> bool:
    if not url:
        return False
    pattern = r'^https?://(www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+/?$'
    return bool(re.match(pattern, url))