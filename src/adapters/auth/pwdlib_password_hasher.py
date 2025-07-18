from pwdlib import PasswordHash

from src.domain.ports.hash_service import HashService


class PwdlibPasswordHasher(HashService):
    def __init__(self):
        self.hasher = PasswordHash.recommended()

    def hash_password(self, password: str) -> str:
        return self.hasher.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.hasher.verify(password, hashed_password)
