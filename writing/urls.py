from django.urls import path
from writing.views import SubmitWritingTask

urlpatterns = [
    path('check-essay/',SubmitWritingTask.as_view(),name="check-essay")
]