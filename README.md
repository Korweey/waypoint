# Waypoint — Trail Finder

A trail-finder and trip-planner web app built with Django.
Developer: Qawiyy Rabiu — N10038749
Course: Application Programming CCGC 5003 (Individual Term Project, Weeks 7–14)

## What it does

Waypoint catalogs hiking trails, grouped into parks, with a public browsing
catalog, a trail detail page, a trail-report form, and a search page. Trail
and Park data is managed through the Django admin.

## Requirements

* Python 3.14
* Django 6.1

**Note on Django version:** this project uses Django 6.1 rather than the
originally suggested 4.2. This was a deliberate choice — 6.1 was already
installed in the working environment, was confirmed to run all migrations,
system checks, and tests cleanly, and no compatibility issues were
encountered during development.

## Setup \& Running

1. Clone the repository:

```
   git clone https://github.com/Korweey/waypoint
   cd waypoint
   ```

2. Create and activate a virtual environment:

```
   python -m venv .venv
   .venv\\Scripts\\Activate.ps1      # Windows PowerShell
   source .venv/bin/activate       # macOS/Linux
   ```

3. Install dependencies:

```
   pip install -r requirements.txt
   ```

4. Apply database migrations:

```
   python manage.py migrate
   ```

5. Create a superuser (for admin access):

```
   python manage.py createsuperuser
   ```

6. Run the development server:

```
   python manage.py runserver
   ```

7. Open your browser to:

   * Catalog: `http://127.0.0.1:8000/trails/`
   * Admin: `http://127.0.0.1:8000/admin/`

The database starts empty — add Parks and Trails through the admin, or see
`seed\_trails.py` / `seed\_parks.py` in the project root for sample data you
can load via `python manage.py shell` (paste the script contents in, or run
`exec(open('seed\_trails.py').read())` at the `>>>` prompt).

## Running Tests

```
python manage.py test
```

This runs the trails app's test suite (`trails/tests.py`), covering:

* The catalog view only returns open trails
* The trail detail view returns 200 for a real trail and 404 for an unknown one
* Domain rules on the `Distance` value type (`waypoint\_core/distance.py`) —
rejecting negative magnitudes and correctly converting mixed units

## Project Structure

```
waypoint/
├── manage.py
├── requirements.txt
├── waypoint\_site/       # Project settings, root URL config
├── trails/              # Main app: models, views, templates, tests
│   ├── models.py        # Trail, Park
│   ├── views.py         # catalog, detail, report, search, park\_trails
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   └── templates/trails/
├── templates/            # Shared base.html + partials (navbar, footer)
├── static/                # style.css
└── waypoint\_core/        # Standalone domain package (Distance, Trail
                           # class hierarchy) from Weeks 7-8, independent
                           # of Django
```

## Routes

|URL|Description|
|-|-|
|`/trails/`|Trail catalog (open trails, ordered by distance)|
|`/trails/<id>/`|Single trail detail page|
|`/trails/parks/<id>/`|Trails belonging to a specific park|
|`/trails/report/`|Trail report form (CSRF-protected)|
|`/trails/search/`|Trail search|
|`/trails/about/`|About page|
|`/admin/`|Django admin (manage Trails and Parks)|

## Screenshots

*\*\*Trail Catalogue\*\**

*!\[Trail catalog](screenshots/catalog.png)*



*\*\*Admin — Trails app\*\**

*!\[Admin](screenshots/admin.png)*



## AI Assistance

This project was built with Claude AI assistance throughout Weeks 9–14 —
debugging Django setup issues (a circular URL include causing a
RecursionError, missing view functions, template path structure),
drafting views/models/templates/tests against each week's acceptance
criteria, and reviewing git workflow (branching, PRs, tagging) at each
checkpoint. All code was reviewed, tested, and understood before merging.

