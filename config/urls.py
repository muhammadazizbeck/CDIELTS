from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
   openapi.Info(
      title="CD IELTS API",
      default_version='v1',
      description="Test description",
      terms_of_service="Terms and Services",
      contact=openapi.Contact(email="aa2004bek@gmail.com"),
      license=openapi.License(name="CD IELTS License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# urls.py
from django.http import HttpResponse
from django.urls import path

def test_https(request):
    return HttpResponse(f"X-Forwarded-Proto: {request.META.get('HTTP_X_FORWARDED_PROTO')}")




urlpatterns = [
   path('foradmins-only/', admin.site.urls),
   path("api/users/",include("users.urls")),
   path('api/writing/',include("writing.urls")),
   path("api/article/",include('article.urls')),
   path("test-https/", test_https),
   path("api/dictionary/",include('dictionary.urls')),
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
