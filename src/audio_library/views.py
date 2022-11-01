import os.path

from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, parsers
from rest_framework.views import APIView

from . import models, serializers
from .classes import MixedSerializer, Pagination
from ..base.permissions import IsAuthor
from ..base.services import delete_old_file


class GenreView(generics.ListAPIView):
    """Список жанров"""
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializers


class LicenseView(viewsets.ModelViewSet):
    """CRUD лицензий автора"""
    serializer_class = serializers.LicenseSerializers
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return models.License.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AlbumView(viewsets.ModelViewSet):
    """CRUD альбомов автора"""
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializers.AlbumSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return models.Album.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class PublicAlbumView(generics.ListAPIView):
    """Список публичных альбовов автора"""
    serializer_class = serializers.AlbumSerializer

    def get_queryset(self):
        return models.Album.objects.filter(user__id=self.kwargs.get('pk'), private=False)


class TrackView(MixedSerializer, viewsets.ModelViewSet):
    """CRUD треков"""
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [IsAuthor]
    serializer_class = serializers.CreateAuthorSerializer
    serializer_classes_by_action = {
        'list': serializers.AuthorTrackSerializer
    }

    def get_queryset(self):
        return models.Track.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class PlayListView(MixedSerializer, viewsets.ModelViewSet):
    """CRUD плейлистов пользователя"""
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [IsAuthor]
    serializer_class = serializers.CreatePlayListSerializer

    serializer_classes_by_action = {
        'list': serializers.CreatePlayListSerializer
    }

    def get_queryset(self):
        return models.PlayList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class TrackListView(generics.ListAPIView):
    """Список всех треков"""
    queryset = models.Track.objects.all()
    serializer_class = serializers.AuthorTrackSerializer
    pagination_class = Pagination


class AuthorTrackListView(generics.ListAPIView):
    """Список всех треков автора"""
    serializer_class = serializers.AuthorTrackSerializer
    pagination_class = Pagination

    def get_queryset(self):
        return models.Track.objects.filter(user__id=self.kwargs.get('pk'))


class StreamingFileView(APIView):
    """Воспроизведение трека"""

    def set_play(self, track):
        track.plays_count += 1
        track.save()

    def get(self, request, pk):
        track = get_object_or_404(models.Track, id=pk)
        if os.path.exists(track.file.path):
            self.set_play(track)
            return FileResponse(open(track.file.path, 'rb'), filename=track.file.name)
        else:
            return Http404


class DownloadTrackView(APIView):
    """Скачивание трека"""

    def set_download(self):
        self.track.download += 1
        self.track.save()

    def get(self, request, pk):
        self.track = get_object_or_404(models.Track, id=pk)
        if os.path.exists(self.track.file.path):
            self.set_download()
            return FileResponse(
                open(self.track.file.path, 'rb'), filename=self.track.file.name, as_attachment=True
            )
        else:
            return Http404