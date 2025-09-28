from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1> Welcome to Online  Poll Backend</h1><p>Visit /api/docs/ for API documentation.</p>")
