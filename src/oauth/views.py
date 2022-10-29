from django.shortcuts import render
from rest_framework import viewsets, parsers, permissions

# Create your views here.
from src.base.permissions import IsAuthor
from src.oauth.models import AuthUser
from src.oauth.serializers import UsersSerializer, AuthorSerializer, SocialLinkSerializer


class UserView(viewsets.ModelViewSet):
    """Просмотр и редактирование данных пользователя"""
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.get_queryset()


class AuthorView(viewsets.ReadOnlyModelViewSet):
    """Список авторов"""
    queryset = AuthUser.objects.all().prefetch_related('social_links')
    serializer_class = AuthorSerializer


class SocialLinkView(viewsets.ModelViewSet):
    """CRUD ссылок соц. сетей пользователя"""
    serializer_class = SocialLinkSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return self.request.user.social_links.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

