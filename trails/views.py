"""
trails/views.py
----------------
Views for the trails app.

Week 9:
index()  — renders the homepage/catalog with a welcome message
           and a hard-coded list of sample trails passed
           as template context.
about()  — renders a simple about page.

Week 10:
report() — GET renders a blank trail-report form;
           POST reads the submitted data and renders
           a personalized thank-you page.
search() — safely reads an optional 'q' query param
           and renders the search page.

Week 11:
index() now serves as the trail catalog: each trail dict
includes distance_km (numeric, for floatformat filtering),
elevation_gain, and is_open — used by the template to badge
closed/hard trails and number rows with forloop.counter.
"""

from django.shortcuts import render

# Sample trail data — hard-coded for Weeks 9-11.
# Week 12 will replace this with database queries.
SAMPLE_TRAILS = [
    {
        'id':             1,
        'name':           'Ridgeline Loop',
        'distance_km':    8.5,
        'elevation_gain': 450,
        'difficulty':     'hard',
        'type':           'DayHike',
        'is_open':        True,
    },
    {
        'id':             2,
        'name':           'Coastal Traverse',
        'distance_km':    30.0,
        'elevation_gain': 1200,
        'difficulty':     'expert',
        'type':           'BackpackingRoute',
        'is_open':        True,
    },
    {
        'id':             3,
        'name':           'Speed Loop',
        'distance_km':    12.0,
        'elevation_gain': 300,
        'difficulty':     'moderate',
        'type':           'TrailRun',
        'is_open':        True,
    },
    {
        'id':             4,
        'name':           'Summit Push',
        'distance_km':    10.0,
        'elevation_gain': 900,
        'difficulty':     'hard',
        'type':           'GuidedDayHike',
        'is_open':        False,
    },
    {
        'id':             5,
        'name':           'Meadow Walk',
        'distance_km':    5.25,
        'elevation_gain': 120,
        'difficulty':     'easy',
        'type':           'DayHike',
        'is_open':        True,
    },
    {
        'id':             6,
        'name':           'Alpine Traverse',
        'distance_km':    22.75,
        'elevation_gain': 1600,
        'difficulty':     'expert',
        'type':           'BackpackingRoute',
        'is_open':        False,
    },
]


def index(request):
    """
    Homepage / catalog view — renders the trail listing page.

    Parameters:
        request (HttpRequest) : The incoming HTTP request.

    Returns:
        HttpResponse: Rendered trails/index.html template.
    """
    context = {
        'page_title': 'Waypoint — Find Your Trail',
        'trails':     SAMPLE_TRAILS,
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
