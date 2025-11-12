from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import WritingTask, WritingSubmission, WritingEvaluation
from .serializers import WritingSubmissionSerializer, WritingTaskSerializer
from .openai import evaluate_with_openai

class SubmitAndEvaluateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        task_id = request.data.get('task_id')
        answer = request.data.get('answer', '').strip()

        if not task_id:
            return Response({"error": "task_id majburiy!"}, status=400)
        if len(answer) < 50:
            return Response({"error": "Essay juda qisqa!"}, status=400)

        task = get_object_or_404(WritingTask, id=task_id)

        submission = WritingSubmission.objects.create(
            user=request.user,
            task=task,
            answer=answer
        )

        # OpenAI bilan baholash
        eval_data = evaluate_with_openai(submission)
        WritingEvaluation.objects.create(submission=submission, **eval_data)

        serializer = WritingSubmissionSerializer(submission)
        return Response({
            "success": True,
            "message": "Essay yuborildi va OpenAI baholadi!",
            "submission_id": submission.id,
            "band_score": eval_data['score'],
            "data": serializer.data
        }, status=201)

class WritingTaskAPIView(APIView):
    def get(self,request):
        writing_tasks = WritingTask.objects.all()
        serializer = WritingTaskSerializer(writing_tasks,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    


