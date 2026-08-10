"""
waypoint_core/test_week7.py
----------------------------
Quick tests verifying all Week 7 acceptance criteria.

Run from the waypoint/ root folder with:
    python -m waypoint_core.test_week7
"""

from waypoint_core.distance import Distance
from waypoint_core.trail    import Trail, Itinerary


def test_distance_rejects_negative():
    """Distance must raise ValueError for negative magnitude."""
    try:
        Distance(-1, 'km')
        print("FAIL — negative distance was accepted")
    except ValueError:
        print("PASS — Distance rejects negative magnitude")


def test_distance_convert_roundtrip():
    """convert() round-trips within a small tolerance."""
    d        = Distance(5, 'km')
    d_mi     = d.convert()
    d_back   = d_mi.convert()
    diff     = abs(d_back.magnitude - d.magnitude)
    if diff < 0.001:
        print(f"PASS — round-trip: {d} -> {d_mi} -> {d_back}")
    else:
        print(f"FAIL — round-trip off by {diff}")


def test_trail_from_dict():
    """from_dict() builds a Trail correctly."""
    data = {
        'id': 1, 'name': 'Ridgeline Loop',
        'distance': 8.5, 'unit': 'km',
        'elevation_gain_m': 320, 'difficulty': 'hard'
    }
    t = Trail.from_dict(data)
    assert t.name             == 'Ridgeline Loop', "name mismatch"
    assert t.distance.magnitude == 8.5,            "distance mismatch"
    assert t.get_difficulty() == 'hard',           "difficulty mismatch"
    print(f"PASS — Trail.from_dict(): {t}")


def test_trail_invalid_difficulty():
    """set_difficulty() raises ValueError for bad input."""
    try:
        Trail(99, 'Bad Trail', Distance(3, 'km'), 100, 'extreme')
        print("FAIL — invalid difficulty was accepted")
    except ValueError:
        print("PASS — Trail rejects invalid difficulty")


def test_trail_equality():
    """Two trails with same id compare equal even if data differs."""
    t1 = Trail(7, 'Trail A', Distance(5, 'km'), 100, 'easy')
    t2 = Trail(7, 'Trail B', Distance(9, 'mi'), 400, 'hard')
    t3 = Trail(8, 'Trail C', Distance(5, 'km'), 100, 'easy')
    if t1 == t2:
        print("PASS — same id => equal")
    else:
        print("FAIL — same id should be equal")
    if t1 != t3:
        print("PASS — different id => not equal")
    else:
        print("FAIL — different id should not be equal")


def test_itinerary_total_distance():
    """Itinerary of three trails reports the correct total."""
    t1 = Trail(1, 'Alpha', Distance(3, 'km'), 100, 'easy')
    t2 = Trail(2, 'Beta',  Distance(4, 'km'), 200, 'moderate')
    t3 = Trail(3, 'Gamma', Distance(5, 'km'), 300, 'hard')

    itin = Itinerary()
    itin.add_trail(t1)
    itin.add_trail(t2)
    itin.add_trail(t3)

    total = itin.total_distance()
    if abs(total.magnitude - 12.0) < 0.001:
        print(f"PASS — total distance: {total}")
    else:
        print(f"FAIL — expected 12 km, got {total}")


def test_itinerary_independence():
    """Adding a trail to one itinerary never changes another."""
    t1 = Trail(1, 'Alpha', Distance(3, 'km'), 100, 'easy')
    t2 = Trail(2, 'Beta',  Distance(4, 'km'), 200, 'moderate')

    itin1 = Itinerary()
    itin2 = Itinerary()

    itin1.add_trail(t1)
    itin2.add_trail(t2)
    itin1.add_trail(t2)   # add to itin1 only

    total1 = itin1.total_distance().magnitude
    total2 = itin2.total_distance().magnitude

    if abs(total1 - 7.0) < 0.001 and abs(total2 - 4.0) < 0.001:
        print("PASS — itineraries are independent")
    else:
        print(f"FAIL — itin1={total1}, itin2={total2}")


def test_default_unit_change():
    """Changing the default unit affects new trails only."""
    Trail.set_default_unit('km')
    t_old = Trail(1, 'Old', Distance(5, 'km'), 100, 'easy')

    Trail.set_default_unit('mi')
    t_new = Trail(2, 'New', Distance(3, 'mi'), 100, 'easy')

    # Reset to km for other tests
    Trail.set_default_unit('km')

    if t_old.distance.unit == 'km' and t_new.distance.unit == 'mi':
        print("PASS — default unit change affects new trails only")
    else:
        print("FAIL — default unit change test")


if __name__ == '__main__':
    print("\n--- Week 7 Acceptance Criteria Tests ---\n")
    test_distance_rejects_negative()
    test_distance_convert_roundtrip()
    test_trail_from_dict()
    test_trail_invalid_difficulty()
    test_trail_equality()
    test_itinerary_total_distance()
    test_itinerary_independence()
    test_default_unit_change()
    print("\n--- All tests complete ---\n")
