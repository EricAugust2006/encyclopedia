from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),  # Adiciona a rota de busca
    path("<str:title>/", views.entry, name="entry"),
]
