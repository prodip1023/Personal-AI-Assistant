import os

class APIKey:
    def __init__(self):
        self.GOOGLE_API_KEY = self._load_api_key()

    @staticmethod
    def _load_api_key() -> str:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        return api_key
