"""
trails/tests.py
-----------------
Tests for the trails app — Week 14 (WP-801).

TrailCatalogTests.test_catalog_shows_only_open_trails
    Confirms the catalog view (index) excludes closed trails —
    this is the query-level filter added in Week 12/13, not just
    template-level hiding.

TrailDetailTests
    test_detail_200_for_existing_trail — sanity check a real trail
    renders correctly.
    test_detail_404_for_unknown_trail — confirms requesting a trail
    id that doesn't exist returns a standard 404, rather than
    raising an unhandled exception. This is what get_object_or_404
    in trail_detail() is responsible for.

DistanceDomainRuleTests
    Unit tests against waypoint_core.distance.Distance (Week 7/8
    domain logic), imported directly rather than relying on
    Django's test discovery to also pick up the standalone
    waypoint_core/test_week7.py and test_week8.py files.

    test_negative_magnitude_raises_value_error — Distance rejects
    negative magnitudes at construction.
    test_mixed_unit_addition_converts_to_left_operand_unit —
    Distance.__add__ auto-converts the right-hand operand to the
    left operand's unit before summing.

Run with:
    python manage.py test
"""

from django.test import TestCase
from django.urls import reverse
from .models import Trail
from waypoint_core.distance import Distance


class TrailCatalogTests(TestCase):
    def setUp(self):
        self.open_trail = Trail.objects.create(
            name='Open Sample Trail',
            distance_km=5.00,
            elevation_gain=100,
            difficulty='easy',
            is_open=True,
        )
        self.closed_trail = Trail.objects.create(
            name='Closed Sample Trail',
            distance_km=7.50,
            elevation_gain=200,
            difficulty='hard',
            is_open=False,
        )

    def test_catalog_shows_only_open_trails(self):
        response = self.client.get(reverse('trails:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.open_trail.name)
        self.assertNotContains(response, self.closed_trail.name)


class TrailDetailTests(TestCase):
    def setUp(self):
        self.trail = Trail.objects.create(
            name='Detail Test Trail',
            distance_km=3.20,
            elevation_gain=50,
            difficulty='moderate',
            is_open=True,
        )

    def test_detail_200_for_existing_trail(self):
        response = self.client.get(
            reverse('trails:trail_detail', args=[self.trail.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.trail.name)

    def test_detail_404_for_unknown_trail(self):
        nonexistent_id = self.trail.id + 9999
        response = self.client.get(
            reverse('trails:trail_detail', args=[nonexistent_id])
        )
        self.assertEqual(response.status_code, 404)


class DistanceDomainRuleTests(TestCase):
    def test_negative_magnitude_raises_value_error(self):
        with self.assertRaises(ValueError):
            Distance(-1, 'km')

    def test_mixed_unit_addition_converts_to_left_operand_unit(self):
        five_km = Distance(5, 'km')
        one_mile = Distance(1, 'mi')
        result = five_km + one_mile

        self.assertEqual(result.unit, 'km')
        # 1 mile == 1.60934 km, so 5 km + 1 mi == 6.60934 km
        self.assertAlmostEqual(result.magnitude, 6.60934, places=3)
