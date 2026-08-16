"""
trails/models.py
------------------
Trail and Park models.

Week 12: Trail model.
Week 13: Park model added, with Trail.park as a ForeignKey.

on_delete / null strategy for Trail.park (WP-702):
    on_delete=models.SET_NULL — if a Park record is ever deleted, its
    trails are NOT deleted with it. A trail is a real physical place;
    it still exists whether or not we keep an administrative "park"
    grouping for it in this database. Cascading deletes here would
    destroy trail data as a side effect of deleting an unrelated Park
    record, which is not acceptable.

    null=True, blank=True — required for SET_NULL to be valid, and also
    lets existing Trail rows (created in Week 12, before Park existed)
    migrate cleanly with park=NULL rather than needing a manufactured
    default Park assigned to every historical row.
"""

from django.db import models


class Park(models.Model):
    """
    A park that groups one or more trails.

    Fields:
        name   : Park name.
        region : Region or general location (e.g. "Muskoka, ON").
    """

    name   = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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
        park           : The Park this trail belongs to (optional — see
                         module docstring for the on_delete/null reasoning).
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
    park           = models.ForeignKey(
        Park,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name
