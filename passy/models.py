from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User

from typing import List, Dict, Any, Optional

from django.shortcuts import get_object_or_404

import common.crypto


# Django makes us specify the max_length of CharField's, we chose to use a value that will work on all databases and should be enough
# for all our usages:
MAX_CHAR_FIELD = 255


class StoredPassword(models.Model):

    site: str = models.CharField(max_length=MAX_CHAR_FIELD)

    data: bytes = models.BinaryField()
    salt: bytes = models.BinaryField()

    owner: User = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.site

    def set(self, password: str, master_password: str) -> None:

        self.salt = common.crypto.generate_salt()
        crypter = common.crypto.get_crypter(master_password=master_password, salt=self.salt)
        self.data = crypter.encrypt(password.encode())

    def get(self, master_password: str) -> str:

        crypter = common.crypto.get_crypter(master_password=master_password, salt=self.salt)

        password = crypter.decrypt(self.data).decode()

        return password


def get_passwords(**kwargs: Dict[str, Any]) -> List[StoredPassword]:
    return StoredPassword.objects.filter(**kwargs)


def get_password(**kwargs: Dict[str, Any]) -> StoredPassword:
    return get_object_or_404(StoredPassword, **kwargs)


def get_user_or_none(**kwargs: Dict[str, Any]) -> Optional[User]:

    try:
        return User.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None
