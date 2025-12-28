import os
from dotenv import load_dotenv

load_dotenv()  


class APIKey:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found")

    def load_api_key(self):
        return self.api_key

