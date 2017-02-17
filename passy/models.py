import os
import base64

from django.db import models
from django.contrib.auth.models import User

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from typing import List, Dict, Any

from django.shortcuts import get_object_or_404


def generate_salt() -> bytes:
    return os.urandom(32)


def get_crypter(master_password: str, salt: bytes) -> Fernet:

    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000,
                     backend=default_backend())

    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

    return Fernet(key)


class StoredPassword(models.Model):

    site: str = models.CharField(max_length=200, unique=True)

    data: bytes = models.BinaryField(max_length=200)
    salt: bytes = models.BinaryField(max_length=200)

    owner: User = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.site

    def set(self, password: str, master_password: str) -> None:

        self.salt = generate_salt()
        crypter = get_crypter(master_password=master_password, salt=self.salt)
        self.data = crypter.encrypt(password.encode())

    def get(self, master_password: str) -> str:

        crypter = get_crypter(master_password=master_password, salt=self.salt)

        password = crypter.decrypt(self.data).decode()

        return password


def get_users(**kwargs: Dict[str, Any]) -> List[User]:
    return User.objects.filter(**kwargs)


def get_user(**kwargs: Dict[str, Any]) -> User:
    return get_object_or_404(User, **kwargs)


def get_passwords(**kwargs: Dict[str, Any]) -> List[StoredPassword]:
    return StoredPassword.objects.filter(**kwargs)


def get_password(**kwargs: Dict[str, Any]) -> StoredPassword:
    return get_object_or_404(StoredPassword, **kwargs)
