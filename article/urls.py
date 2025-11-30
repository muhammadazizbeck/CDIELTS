from django.urls import path,include
from .views import ArticleAPIView,ArticleRetrieveAPIView

urlpatterns = [
    path('articles/',ArticleAPIView.as_view(),name='articles'),
    path('articles/<int:pk>/',ArticleRetrieveAPIView.as_view(),name='article')
]