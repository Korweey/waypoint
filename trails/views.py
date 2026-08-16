"""
trails/views.py
----------------
Views for the trails app.

Week 9:
about()  — renders a simple about page.

Week 10:
report() — GET renders a blank trail-report form;
           POST reads the submitted data and renders
           a personalized thank-you page.
search() — safely reads an optional 'q' query param
           and renders the search page.

Week 11:
index()  — renders the trail catalog using the shared base.html
           partials, with badges and forloop.counter handled in
           the template.

Week 12:
index() now queries the Trail model instead of a hard-coded list.
Only open trails are shown, ordered by distance — the Week 11
template renders these model instances with no changes required.

Week 13:
park_trails() — cross-relation query: given a park id, shows only
                the open trails belonging to that park, reusing the
                same catalog template with a customized heading.
"""

from django.shortcuts import render, get_object_or_404
from .models import Trail, Park


def index(request):
    """
    Homepage / catalog view — renders the trail listing page.

    Queries only open trails from the database, ordered by
    distance_km ascending. Closed trails are excluded here in
    the query itself, not just hidden in the template.

    Parameters:
        request (HttpRequest) : The incoming HTTP request.

    Returns:
        HttpResponse: Rendered trails/index.html template.
    """
    trails = Trail.objects.filter(is_open=True).order_by('distance_km')
    context = {
        'page_title': 'Waypoint — Find Your Trail',
        'heading':    'Trail Catalogue',
        'trails':     trails,
    }
    return render(request, 'trails/index.html', context)


def park_trails(request, park_id):
    """
    Cross-relation query view — shows only the open trails that
    belong to a specific park.

    Parameters:
        request (HttpRequest) : The incoming HTTP request.
        park_id (int)         : Primary key of the Park to filter by.

    Returns:
        HttpResponse: Rendered trails/index.html template, reused
                       unmodified with a park-specific heading.
    """
    park = get_object_or_404(Park, pk=park_id)
    trails = Trail.objects.filter(park=park, is_open=True).order_by('distance_km')
    context = {
        'page_title': f'Trails in {park.name}',
        'heading':    f'Trails in {park.name}',
        'trails':     trails,
    }
    return render(request, 'trails/index.html', context)


def about(request):
    """
    About page view — renders a simple about page.

    Parameters:
        request (HttpRequest) : The incoming HTTP request.

    Returns:
        HttpResponse: Rendered trails/about.html template.
    """
    context = {
        'page_title': 'About Waypoint',
        'developer':  'Qawiyy Rabiu',
        'student_id': 'N10038749',
        'course':     'Application Programming CCGC 5003',
    }
    return render(request, 'trails/about.html', context)


def report(request):
    """
    Trail report view.

    GET  -> renders a blank report form.
    POST -> reads submitted data, renders a personalized thank-you.

    Parameters:
        request (HttpRequest) : The incoming HTTP request.

    Returns:
        HttpResponse: Rendered trails/report.html (GET) or
                       trails/report_thanks.html (POST).
    """
    if request.method == 'POST':
        name  = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        trail = request.POST.get('trail', '').strip()
        note  = request.POST.get('note', '').strip()

        context = {
            'page_title': 'Thanks for your report!',
            'name':       name,
            'email':      email,
            'trail':      trail,
            'note':       note,
        }
        return render(request, 'trails/report_thanks.html', context)

    context = {'page_title': 'Report a Trail'}
    return render(request, 'trails/report.html', context)


def search(request):
    """
    Search view — safely reads an optional 'q' query param.

    Parameters:
        request (HttpRequest) : The incoming HTTP request.

    Returns:
        HttpResponse: Rendered trails/search.html template.
    """
    query = request.GET.get('q', '')
    context = {
        'page_title': 'Search Trails',
        'query':      query,
    }
    return render(request, 'trails/search.html', context)
