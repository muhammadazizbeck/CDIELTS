from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from writing.models import WritingCheck
from .serializers import WritingTaskSerializer
import requests
from django.conf import settings

class SubmitWritingTask(APIView):
    permission_classes = [AllowAny]

    def post(self, request, task_id):
        try:
            task = WritingCheck.objects.get(id=task_id)
        except WritingCheck.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = WritingTaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            task = serializer.save(user=request.user)

            payload = {"text": task.text}
            if task.task_type == 'task1' and task.image:
                payload['image_url'] = request.build_absolute_uri(task.image.url)

            grok_api_url = settings.GROK_API_URL
            headers = {"Authorization": f"Bearer {settings.GROK_API_KEY}"}
            response = requests.post(grok_api_url, json=payload, headers=headers)

            if response.status_code == 200:
                data = response.json()
                task.score = data.get("score")
                task.coherence = data.get("coherence")
                task.grammar = data.get("grammar")
                task.vocabulary = data.get("vocabulary")
                task.response = data.get("task_response")
                task.feedback = data.get("feedback")
                task.save()
                return Response(WritingTaskSerializer(task).data)
            else:
                return Response({"error": "Grok API error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

