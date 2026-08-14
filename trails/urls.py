"""
trails/urls.py
----------------------
App-level URL configuration for the trails app.
Mounted at '/' by waypoint_site/urls.py.

Routes:
    ''          -> index (trail catalog)
    'about/'    -> about
"""

from django.urls import path
from . import views

app_name = 'trails'

urlpatterns = [
    path('',        views.index, name='index'),
    path('about/',  views.about, name='about'),
]