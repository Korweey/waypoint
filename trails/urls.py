"""
trails/urls.py
---------------
URL configuration for the trails app.

Routes:
    /          -> homepage view (index)
    /about/    -> about page view
    /report/   -> trail report form (GET) / submission (POST)
    /search/   -> trail search view
"""

from django.urls import path
from trails      import views

app_name = 'trails'

urlpatterns = [
    path('',        views.index,  name='index'),
    path('about/',  views.about,  name='about'),
    path('report/', views.report, name='report'),
    path('search/', views.search, name='search'),
]
