import os
import json
import hashlib
import hmac
from typing import Dict


class AuthManager:
    def __init__(self, path: str = "data/users.json"):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

        if not os.path.exists(self.path):
            self._save({})

    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        """Return salted SHA256 hash"""
        return hashlib.sha256(f"{salt}{password}".encode("utf-8")).hexdigest()

    @staticmethod
    def _generate_salt(username: str) -> str:
        return hashlib.sha256(username.encode()).hexdigest()[:16]

    def register(self, username: str, password: str) -> bool:
        if not username or not password:
            return False

        users = self._load()
        if username in users:
            return False

        salt = self._generate_salt(username)
        users[username] = {
            "salt": salt,
            "password": self._hash_password(password, salt)
        }

        self._save(users)
        return True

    def login(self, username: str, password: str) -> bool:
        users = self._load()
        user = users.get(username)

        if not user:
            return False

        expected = user["password"]
        actual = self._hash_password(password, user["salt"])

        return hmac.compare_digest(expected, actual)

    def _load(self) -> Dict:
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, users: Dict):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2)
