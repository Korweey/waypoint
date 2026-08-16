# Seed data for Week 13 — run inside `python manage.py shell`
# Paste this whole block in.
#
# Assumes Week 12's 6 trails already exist (created via the Week 12
# seed_trails.py). This script creates 2 parks and assigns 4 of the
# 6 trails to them, leaving 2 unassigned (park=None) to demonstrate
# the null strategy.

from trails.models import Trail, Park

Park.objects.all().delete()

ridge_park  = Park.objects.create(name='Ridgeline Provincial Park', region='Muskoka, ON')
coast_park  = Park.objects.create(name='Coastal Headlands Park',    region='Bruce Peninsula, ON')

def assign(name, park):
    try:
        trail = Trail.objects.get(name=name)
        trail.park = park
        trail.save()
        print(f"Assigned {name} -> {park.name}")
    except Trail.DoesNotExist:
        print(f"Skipped {name} — not found (run the Week 12 seed script first)")

assign('Ridgeline Loop',   ridge_park)
assign('Summit Push',      ridge_park)
assign('Coastal Traverse', coast_park)
assign('Alpine Traverse',  coast_park)
# Speed Loop and Meadow Walk intentionally left unassigned (park=None)

print(f"Parks: {Park.objects.count()}, Trails with a park: {Trail.objects.exclude(park=None).count()}")
