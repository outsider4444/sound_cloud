from rest_framework import serializers
from . import models


class BaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)


class GenreSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ('id', 'name', )


class LicenseSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.License
        fields = ('id', 'text', )
