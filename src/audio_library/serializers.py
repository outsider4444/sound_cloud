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


class CreateAuthorSerializer(BaseSerializer):
    plays_count = serializers.IntegerField(read_only=True)
    download = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Track
        fields = (
            'id',
            'title',
            'license',
            'genre',
            'album',
            'link_of_author',
            'file',
            'create_at',
            'plays_count',
            'download',
        )

    def update(self, instance, validated_data):
        delete_old_file(instance.file.path)
        return super().update(instance, validated_data)


class AuthorTrackSerializer(CreateAuthorSerializer):
    license = LicenseSerializers()
    genre = GenreSerializers(many=True)
    album = AlbumSerializer()


class CreatePlayListSerializer(BaseSerializer):
    class Meta:
        model = models.PlayList
        fields = ('id', 'title', 'cover', 'tracks')

    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class PlayListSerializer(CreatePlayListSerializer):
    tracks = AuthorTrackSerializer(many=True, read_only=True)


# todo Вывод текста песни (если есть).
# todo Вывод автора