"""
waypoint_core/test_week8.py
----------------------------
Tests for Week 8 acceptance criteria.

Run from the waypoint/ root with:
    python -m waypoint_core.test_week8
"""

from waypoint_core.distance   import Distance
from waypoint_core.trail_types import (
    Trail, DayHike, GuidedDayHike,
    BackpackingRoute, TrailRun, FakeTrail
)


def test_polymorphic_loop():
    """One loop prints estimated_time() for each trail type."""
    print("\n--- Polymorphic loop ---")
    trails = [
        DayHike(1, 'Ridgeline', Distance(8, 'km'), 400, 'hard'),
        BackpackingRoute(2, 'Coastal', Distance(30, 'km'), 1200, 'expert', num_days=3),
        TrailRun(3, 'Speed Loop', Distance(12, 'km'), 300, 'moderate'),
        GuidedDayHike(4, 'Summit', Distance(10, 'km'), 600, 'hard', 'Jane'),
        FakeTrail('Test Trail'),
    ]
    for t in trails:
        print(f"  {t.summary()} | estimated_time: {t.estimated_time()} h")
    print("PASS — polymorphic loop ran for all trail types including FakeTrail")


def test_distance_operators():
    """Distance arithmetic and comparison operators."""
    d1 = Distance(3, 'km')
    d2 = Distance(2, 'km')

    # Addition
    result = d1 + d2
    assert abs(result.magnitude - 5.0) < 1e-6, f"Add failed: {result}"
    print(f"PASS — {d1} + {d2} = {result}")

    # Subtraction
    result = d1 - d2
    assert abs(result.magnitude - 1.0) < 1e-6, f"Sub failed: {result}"
    print(f"PASS — {d1} - {d2} = {result}")

    # Equality
    d3 = Distance(3, 'km')
    assert d1 == d3, "Equality failed"
    print(f"PASS — {d1} == {d3}")

    # Less than / greater than
    assert d2 < d1, "Less-than failed"
    assert d1 > d2, "Greater-than failed"
    print(f"PASS — {d2} < {d1} and {d1} > {d2}")

    # Sort a list using <
    distances = [Distance(5,'km'), Distance(2,'km'), Distance(8,'km')]
    sorted_d  = sorted(distances)
    mags      = [d.magnitude for d in sorted_d]
    assert mags == sorted(mags), f"Sort failed: {mags}"
    print(f"PASS — sorted distances: {[str(d) for d in sorted_d]}")


def test_mixed_unit_operators():
    """Mixed units are auto-converted before operations."""
    d_km = Distance(5, 'km')
    d_mi = Distance(1, 'mi')   # ~1.609 km
    result = d_km + d_mi
    assert result.unit == 'km', f"Result unit should be km, got {result.unit}"
    assert abs(result.magnitude - (5 + 1.60934)) < 0.001, f"Mixed add failed: {result}"
    print(f"PASS — mixed units: {d_km} + {d_mi} = {result}")


def test_abstract_trail_raises():
    """Instantiating Trail directly raises TypeError."""
    try:
        Trail(1, 'Test', Distance(5, 'km'), 100, 'easy')
        print("FAIL — Trail should not be instantiatable directly")
    except TypeError:
        print("PASS — Trail() raises TypeError (abstract)")


def test_missing_abstract_method_raises():
    """A subclass missing estimated_time() raises TypeError."""
    try:
        class BrokenTrail(Trail):
            def summary(self):
                return "broken"
        BrokenTrail(1, 'x', Distance(1,'km'), 0, 'easy')
        print("FAIL — BrokenTrail should raise TypeError")
    except TypeError:
        print("PASS — subclass missing estimated_time() raises TypeError")


def test_mro():
    """Show MRO for GuidedDayHike (composed with mixins)."""
    mro_names = [c.__name__ for c in GuidedDayHike.__mro__]
    print(f"\nGuidedDayHike MRO: {mro_names}")
    assert 'GuidedDayHike' in mro_names
    assert 'DayHike'       in mro_names
    assert 'ElevationMixin' in mro_names
    assert 'RatingMixin'   in mro_names
    assert 'Trail'         in mro_names
    print("PASS — MRO contains all expected classes")


def test_guided_day_hike():
    """GuidedDayHike adds guide_name and extends summary."""
    g = GuidedDayHike(10, 'Summit Push', Distance(6,'km'),
                      300, 'hard', 'Jane Smith')
    assert g.guide_name == 'Jane Smith'
    assert 'Jane Smith' in g.summary()
    assert 'GuidedDayHike' in g.summary()
    print(f"PASS — GuidedDayHike: {g.summary()}")


def test_elevation_mixin():
    """ElevationMixin.grade_percent() returns correct value."""
    d = DayHike(5, 'Steep', Distance(2, 'km'), 200, 'hard')
    grade = d.grade_percent()
    # 200m gain / 2000m distance * 100 = 10%
    assert abs(grade - 10.0) < 0.01, f"Grade wrong: {grade}"
    print(f"PASS — grade_percent: {grade}%")


def test_rating_mixin():
    """RatingMixin.add_rating() and average_rating() work."""
    d = DayHike(6, 'Rated', Distance(5,'km'), 100, 'easy')
    d.add_rating(4)
    d.add_rating(5)
    avg = d.average_rating()
    assert abs(avg - 4.5) < 0.01, f"Average wrong: {avg}"
    print(f"PASS — average_rating: {avg} stars")


def test_fake_trail_in_loop():
    """FakeTrail works in the polymorphic loop unchanged."""
    fake = FakeTrail('Duck Test')
    assert fake.estimated_time() == 1.0
    assert 'FakeTrail' in fake.summary()
    print(f"PASS — FakeTrail: {fake.summary()}")


if __name__ == '__main__':
    print("\n--- Week 8 Acceptance Criteria Tests ---")
    test_polymorphic_loop()
    test_distance_operators()
    test_mixed_unit_operators()
    test_abstract_trail_raises()
    test_missing_abstract_method_raises()
    test_mro()
    test_guided_day_hike()
    test_elevation_mixin()
    test_rating_mixin()
    test_fake_trail_in_loop()
    print("\n--- All Week 8 tests complete ---\n")
