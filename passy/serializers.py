from collections import OrderedDict

from django.db import IntegrityError

from rest_framework import serializers
from rest_framework.request import Request

import common
from . import models


class StoredPassword(serializers.Serializer):

    site = serializers.CharField(max_length=200)
    stored_password_text = serializers.CharField(max_length=200, initial=common.generate_random_password)

    def __init__(self, request: Request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def to_representation(self, instance: models.StoredPassword):
        return OrderedDict(
            site=self.fields['site'].to_representation(instance.site),
            stored_password_text=self.fields['stored_password_text'].to_representation(
                instance.get(master_password=self.request.session['master_password'])
            )
        )

    def create(self, validated_data: dict) -> models.StoredPassword:
        return self.update(models.StoredPassword(), validated_data)

    def update(self, instance: models.StoredPassword, validated_data: dict) -> models.StoredPassword:

        instance.site = validated_data['site']
        instance.owner = self.request.user

        instance.set(validated_data['stored_password_text'], self.request.session['master_password'])

        try:
            instance.save()
        except IntegrityError:
            pass  # todo: Add proper error handling for the errors list..

        return instance


class GeneratedPasswordRequest(serializers.Serializer):

    length = serializers.IntegerField(initial=common.default_password_length, required=True)
    use_symbols = serializers.BooleanField(initial=True, required=True)

    def create(self, validated_data: dict) -> str:
        return self.update(None, validated_data)

    def update(self, instance: None, validated_data: dict) -> str:

        length = validated_data['length']
        use_symbols = validated_data['use_symbols']

        return common.generate_random_password(length=length, use_symbols=use_symbols)
