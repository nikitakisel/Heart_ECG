import string

from django.utils.crypto import get_random_string


def get_random_slug(length: int = 12) -> str:
    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return get_random_string(length, alphabet)
