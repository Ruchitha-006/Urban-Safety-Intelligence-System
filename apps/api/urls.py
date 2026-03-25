from django.urls import path
from . import views

urlpatterns = [
    path('crimes', views.get_crimes),
]