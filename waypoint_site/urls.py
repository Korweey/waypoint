"""
waypoint_site/urls.py
----------------------
Root URL configuration for the Waypoint project.

Routes:
    /trails/    -> trails app (homepage, about, report, search)
    /admin/     -> Django admin site

Week 12: trails app is now mounted at /trails/ instead of the
root, per WP-605.
"""

from django.contrib import admin
from django.urls    import path, include

urlpatterns = [
    path('admin/',  admin.site.urls),
    path('trails/', include('trails.urls')),
]
