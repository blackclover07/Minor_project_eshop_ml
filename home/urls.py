from django.urls import path,include

import home.views

urlpatterns = [
    path('',home.views.index,name='index'),
    path("api/", include("home.api.urls")),
]
