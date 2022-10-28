from django.urls import path

from src.oauth import views

urlpatterns = [
    path('', views.UserView.as_view({'get': 'retrieve', 'put': 'update'})),
    path('author/', views.AuthorView.as_view({'get': 'list'})),
    path('author/<int:pk>', views.AuthorView.as_view({'get': 'retrieve'})),

    path('social/', views.SocialLinkView.as_view({
        'get': 'list', 'post': 'create',
    })),
    path('social/<int:pk>/', views.SocialLinkView.as_view({
        'put': 'update', 'delete': 'destroy'
    })),
]