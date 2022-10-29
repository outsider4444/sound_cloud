from rest_framework import serializers
from . import models
from ..base.services import delete_old_file


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


class AlbumSerializer(BaseSerializer):
    class Meta:
        model = models.Album
        fields = ('id', 'name', 'description', 'cover', 'private')

    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)