# backend/writing/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WritingTaskViewSet, WritingSubmissionViewSet

router = DefaultRouter()
router.register(r'tasks', WritingTaskViewSet, basename='writingtask')
router.register(r'submissions', WritingSubmissionViewSet, basename='writingsubmission')

urlpatterns = [
    path('', include(router.urls)),
]