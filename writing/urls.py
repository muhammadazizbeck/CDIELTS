from django.urls import path
from . import views

urlpatterns = [
    path("writing1-tasks/",views.WritingTask1APIView.as_view(),name='writing1-tasks'),
    path("writing1-tasks/<int:pk>/",views.WritingTask1RetrieveAPIView.as_view(),name="writing1-task"),
    path("writing2-tasks/",views.WritingTask2APIView.as_view(),name='writing2-tasks'),
    path('writing2-tasks/<int:pk>/',views.WritingTask2RetrieveAPIView.as_view(),name='writing2-task'),

    path('writing1/check-report/', views.CheckTask1APIView.as_view(), name='check-task1'),
    path('writing2/check-report/', views.CheckTask2APIView.as_view(), name='check-task2'),
]