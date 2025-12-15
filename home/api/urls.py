from django.urls import path
from .views import ranking_api

urlpatterns = [
    path("ranking/", ranking_api, name="ranking_api"),
]
