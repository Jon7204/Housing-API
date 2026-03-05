import re

def is_postcode(value: str) -> bool:
    postcode_regex = r"^[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}$"
    return bool(re.match(postcode_regex, value.upper()))

def is_postcode_prefix(value: str) -> bool:
    prefix_regex = r"^[A-Z]{1,2}\d?[A-Z\d]?$"
    return bool(re.match(prefix_regex, value.upper()))