"""
waypoint_site/urls.py
----------------------
Root URL configuration for the Waypoint project.

Routes:
    /           -> trails app homepage
    /admin/     -> Django admin site
"""

from django.contrib import admin
from django.urls    import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',       include('trails.urls')),
]