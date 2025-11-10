from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from writing.models import WritingTask
from writing.serializers import WritingTaskSerializer

class WritingTaskAPIView(APIView):
    def get(self,request):
        writing_tasks = WritingTask.objects.all()
        serializer = WritingTaskSerializer(writing_tasks,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

