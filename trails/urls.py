"""
trails/urls.py
---------------
URL configuration for the trails app.

Routes:
    /               -> catalog view (all open trails)
    /about/         -> about page view
    /report/        -> trail report form (GET) / submission (POST)
    /search/        -> trail search view
    /parks/<id>/    -> trails belonging to a specific park (Week 13)
    /<id>/          -> single trail detail page (Week 14)
"""

from django.urls import path
from trails      import views

app_name = 'trails'

urlpatterns = [
    path('',                     views.index,       name='index'),
    path('about/',               views.about,       name='about'),
    path('report/',              views.report,      name='report'),
    path('search/',              views.search,      name='search'),
    path('parks/<int:park_id>/', views.park_trails, name='park_trails'),
    path('<int:trail_id>/',      views.trail_detail, name='trail_detail'),
]
