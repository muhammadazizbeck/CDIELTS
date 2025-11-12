from django.urls import path
from .views import SubmitAndEvaluateAPIView, WritingTaskAPIView

urlpatterns = [
    path("writing-tasks/", WritingTaskAPIView.as_view(), name='writing-tasks'),
    path("submit-and-evaluate/", SubmitAndEvaluateAPIView.as_view(), name='submit-evaluate'),
]