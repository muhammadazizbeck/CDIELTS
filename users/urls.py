from django.urls import path,include
from .views import GoogleAuthRedirect,GoogleCallback

urlpatterns = [
    path("google-auth/",GoogleAuthRedirect.as_view(),name='google-auth'),
    path("google-callback/",GoogleCallback.as_view(),name='google-callback')
]