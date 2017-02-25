from django.db import models
from django.contrib.auth.models import User

from typing import List, Dict, Any

from django.shortcuts import get_object_or_404

import common


class StoredPassword(models.Model):

    site: str = models.CharField(max_length=200)

    data: bytes = models.BinaryField(max_length=200)
    salt: bytes = models.BinaryField(max_length=200)

    owner: User = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.site

    def set(self, password: str, master_password: str) -> None:

        self.salt = common.generate_salt()
        crypter = common.get_crypter(master_password=master_password, salt=self.salt)
        self.data = crypter.encrypt(password.encode())

    def get(self, master_password: str) -> str:

        crypter = common.get_crypter(master_password=master_password, salt=self.salt)

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
