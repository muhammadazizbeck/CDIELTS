from django.urls import path
from . import views

urlpatterns = [
    path("translate/",views.FreeDictionaryAPIView.as_view(),name='translate')
]