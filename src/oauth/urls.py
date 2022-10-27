from django.urls import path

from src.oauth import views

urlpatterns = [
    path('', views.UserView.as_view({
        'get':'retrieve',
        'put':'update',
    }))
]