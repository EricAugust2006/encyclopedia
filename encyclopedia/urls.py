from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),  
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("create_page/", views.create_page, name="createpage"), 
    path("edit/<str:title>/", views.edit_page, name="editpage"),
    path("random_page/", views.random_page, name="randompage"),
    path("deletepage/<str:title>/", views.delete_page, name="deletepage")
]
