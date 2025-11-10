from django.urls import path,include
from writing.views import WritingTaskAPIView

urlpatterns = [
    path("writing-tasks/",WritingTaskAPIView.as_view(),name='writing-tasks')
]