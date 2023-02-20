from django.contrib import admin
from django.urls import path
from .views import *

from django.views.generic import TemplateView


urlpatterns = [
    path("", ProductView.as_view()),
    path("image/", ImageView.as_view()),
]
