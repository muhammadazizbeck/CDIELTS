# views.py
from django.http import HttpResponse

def test_csrf(request):
    return HttpResponse(f"X-Forwarded-Proto: {request.META.get('HTTP_X_FORWARDED_PROTO')} | CSRF_COOKIE_SECURE: {request.COOKIES.get('csrftoken')}")
