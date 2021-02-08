from fastapi import HTTPException


class CommonQueryParams:
    def __init__(self, full: int = 0, no_cache: int = 0, limit: int = 0, as_text: int = 0, comments: int = 0):
        self.full = full
        self.no_cache = no_cache
        self.limit = limit
        self.as_text = as_text
        self.comments = comments


unauthorized = HTTPException(
    status_code=403,
    detail="You cannot access Facebook profiles without enabling USE_ACCOUNT option and logged in.")
