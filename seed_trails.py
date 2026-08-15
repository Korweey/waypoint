# Seed data for Week 12 — run inside `python manage.py shell`
# Paste this whole block in, or run: python manage.py shell < seed_trails.py

from trails.models import Trail

Trail.objects.all().delete()  # start clean if you re-run this

Trail.objects.create(name='Ridgeline Loop',    distance_km=8.50,  elevation_gain=450,  difficulty='hard',     is_open=True)
Trail.objects.create(name='Coastal Traverse',  distance_km=30.00, elevation_gain=1200, difficulty='expert',   is_open=True)
Trail.objects.create(name='Speed Loop',        distance_km=12.00, elevation_gain=300,  difficulty='moderate', is_open=True)
Trail.objects.create(name='Summit Push',       distance_km=10.00, elevation_gain=900,  difficulty='hard',     is_open=False)
Trail.objects.create(name='Meadow Walk',       distance_km=5.25,  elevation_gain=120,  difficulty='easy',     is_open=True)
Trail.objects.create(name='Alpine Traverse',   distance_km=22.75, elevation_gain=1600, difficulty='expert',   is_open=False)

print(f"Seeded {Trail.objects.count()} trails.")
