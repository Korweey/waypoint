"""
trails/admin.py
-----------------
Admin registration for the Trail and Park models.

Week 12: TrailAdmin.
Week 13: ParkAdmin added, with a TrailInline so trails can be assigned
         to a park directly from the Park admin page.
"""

from django.contrib import admin
from .models import Trail, Park


class TrailInline(admin.TabularInline):
    model  = Trail
    extra  = 1
    fields = ('name', 'distance_km', 'difficulty', 'is_open')


@admin.register(Park)
class ParkAdmin(admin.ModelAdmin):
    list_display  = ('name', 'region')
    search_fields = ('name', 'region')
    inlines       = [TrailInline]


@admin.register(Trail)
class TrailAdmin(admin.ModelAdmin):
    list_display  = ('name', 'distance_km', 'elevation_gain', 'difficulty', 'is_open', 'park', 'added')
    search_fields = ('name',)
    list_filter   = ('difficulty', 'is_open', 'park')
