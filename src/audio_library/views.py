import os.path

from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, parsers
from rest_framework.views import APIView

from . import models, serializers
from .classes import MixedSerializer, Pagination
from ..base.permissions import IsAuthor
from ..base.services import delete_old_file

from django_filters.rest_framework import DjangoFilterBackend


class GenreView(generics.ListAPIView):
    """Список жанров"""
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class LicenseView(viewsets.ModelViewSet):
    """CRUD лицензий автора"""
    serializer_class = serializers.LicenseSerializer
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
    serializer_class = serializers.CreateAuthorTrackSerializer
    serializer_classes_by_action = {
        'list': serializers.AuthorTrackSerializer
    }

    def get_queryset(self):
        return models.Track.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        delete_old_file(instance.file.path)
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
    """ Список всех треков"""
    queryset = models.Track.objects.filter(private=False)
    serializer_class = serializers.AuthorTrackSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'user__display_name', 'album__name', 'genre__name']


class AuthorTrackListView(generics.ListAPIView):
    """ Список всех треков автора"""
    serializer_class = serializers.AuthorTrackSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'album__name', 'genre__name']

    def get_queryset(self):
        return models.Track.objects.filter(
            user__id=self.kwargs.get('pk'), album__private=False, private=False
        )


class StreamingFileView(APIView):
    """Воспроизведение трека"""

    def set_play(self):
        self.track.plays_count += 1
        self.track.save()

    def get(self, request, pk):
        self.track = get_object_or_404(models.Track, id=pk, private=False)
        if os.path.exists(self.track.file.path):
            self.set_play()
            response = HttpResponse('', content_type='audio/mpeg', status=206)
            response['X-Accel-Redirect'] = f"/mp3/{self.track.file.name}"
            return response
        else:
            return Http404


class StreamingFileAuthorView(APIView):
    """Воспроизведение своих песен"""
    permission_classes = [IsAuthor]

    def get(self, request, pk):
        self.track = get_object_or_404(models.Track, id=pk, user=request.user)
        if os.path.exists(self.track.file.path):
            response = HttpResponse('', content_type='audio/mpeg', status=206)
            response['X-Accel-Redirect'] = f'/mp3/{self.track.file.name}'
            return response
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
            response = HttpResponse('', content_type='audio/mpeg', status=206)
            response['Content-Disposition'] = f'attachment; filename={self.track.file.name}'
            response['X-Accel-Redirect'] = f'/media/{self.track.file.name}'
            return response
        else:
            return Http404


class AuthorView(viewsets.ModelViewSet):
    """CRUD автора"""
    serializer_class = serializers.AuthorCreateSerializer


class CommentAuthorView(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return models.Comment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentView(viewsets.ModelViewSet):
    """ Комментарии к треку"""
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return models.Comment.objects.filter(track_id=self.kwargs.get('pk'))
