from typing import Generator, Optional
import google.generativeai as genai
from config.settings import APIKey


class GeminiEngine:
    def __init__(self, api_key: Optional[str] = None):
        try:
            self.api_key = api_key or APIKey().GOOGLE_API_KEY
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-2.5-flash")

        except Exception as e:
            raise RuntimeError(f"Failed to initialize GeminiEngine: {e}") from e

    def generate(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip() if response.text else ""
        except Exception as e:
            raise RuntimeError(f"Generation error: {e}") from e

    def stream(self, prompt: str) -> Generator[str, None, None]:
        try:
            response = self.model.generate_content(prompt, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            raise RuntimeError(f"Streaming error: {e}") from e