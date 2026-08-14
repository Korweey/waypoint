"""
trails/views.py
----------------
Views for the trails app — Week 9.

index() — renders the homepage with a welcome message
          and a hard-coded list of sample trails passed
          as template context.

about() — renders a simple about page.

Both views use Django's render() shortcut which loads
the template, fills in the context, and returns an
HttpResponse automatically.
"""

from django.shortcuts import render

# Sample trail data — hard-coded for Week 9.
# Week 12 will replace this with database queries.
SAMPLE_TRAILS = [
    {
        'id':         1,
        'name':       'Ridgeline Loop',
        'distance':   '8.50 km',
        'difficulty': 'hard',
        'type':       'DayHike',
    },
    {
        'id':         2,
        'name':       'Coastal Traverse',
        'distance':   '30.00 km',
        'difficulty': 'expert',
        'type':       'BackpackingRoute',
    },
    {
        'id':         3,
        'name':       'Speed Loop',
        'distance':   '12.00 km',
        'difficulty': 'moderate',
        'type':       'TrailRun',
    },
    {
        'id':         4,
        'name':       'Summit Push',
        'distance':   '10.00 km',
        'difficulty': 'hard',
        'type':       'GuidedDayHike',
    },
]


def index(request):
    """
    Homepage view — renders the trail listing page.

    Passes all sample trails to the template as context
    so the template can loop over them and display each
    trail's name, distance, difficulty, and type.

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