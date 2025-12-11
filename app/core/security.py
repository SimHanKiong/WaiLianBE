from cryptography.fernet import Fernet

from app.core.config import settings


fernet = Fernet(settings.REVERSIBLE_ENCRYPTION_KEY.encode())


def encrypt_reversible(s: str) -> str:
    encrypted = fernet.encrypt(s.encode())
    return encrypted.decode()


def decrypt_reversible(s: str) -> str:
    decrypted = fernet.decrypt(s.encode())
    return decrypted.decode()
