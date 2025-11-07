from django.urls import path,include
from users.views import GoogleAuthRedirect,GoogleAuthCallback

urlpatterns = [
    path("google-auth/",GoogleAuthRedirect.as_view(),name='google-auth'),
    path("google-callback/",GoogleAuthCallback.as_view(),name='google-callback')
]