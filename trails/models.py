"""
trails/models.py
------------------
Trail model — Week 12.

Mirrors the domain fields used by the Week 9-11 hard-coded catalog,
now persisted to the database instead of living in a Python list.
"""

from django.db import models


class Trail(models.Model):
    """
    A single trail entry in the catalog.

    Fields:
        name           : Trail name.
        distance_km    : Distance in kilometres (decimal, to 2 places).
        elevation_gain : Total elevation gain in metres.
        difficulty     : One of DIFFICULTY_CHOICES.
        is_open        : Whether the trail is currently open to hikers.
        added          : Timestamp set automatically when the record is created.
    """

    DIFFICULTY_CHOICES = [
        ('easy',     'Easy'),
        ('moderate', 'Moderate'),
        ('hard',     'Hard'),
        ('expert',   'Expert'),
    ]

    name           = models.CharField(max_length=100)
    distance_km    = models.DecimalField(max_digits=5, decimal_places=2)
    elevation_gain = models.IntegerField()
    difficulty     = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    is_open        = models.BooleanField(default=True)
    added          = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
