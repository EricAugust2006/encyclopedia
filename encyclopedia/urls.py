from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),  
    path("<str:title>/", views.entry, name="entry"),
    path("create_page/", views.create_page, name="create_page"), 
]
