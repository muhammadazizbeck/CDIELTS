# backend/writing/views.py  (TOʻLIQ yangi views.py)
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import WritingTask, WritingSubmission, WritingEvaluation
from .serializers import WritingTaskSerializer, WritingSubmissionSerializer
from .grok_evaluate import evaluate_with_grok
from django.utils import timezone

class WritingTaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WritingTask.objects.all().order_by('-created_at')
    serializer_class = WritingTaskSerializer
    permission_classes = [AllowAny]

class WritingSubmissionViewSet(viewsets.ModelViewSet):
    queryset = WritingSubmission.objects.all()
    serializer_class = WritingSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def evaluate(self, request, pk=None):
        """GROK bilan baholash – ENG MUHIMI!"""
        submission = self.get_object()
        
        if hasattr(submission, 'eval'):
            # Agar allaqachon baholangan boʻlsa
            serializer = self.get_serializer(submission)
            return Response(serializer.data)

        # GROK chaqirish
        try:
            eval_data = evaluate_with_grok(submission)
            evaluation = WritingEvaluation.objects.create(
                submission=submission,
                **eval_data
            )
            serializer = self.get_serializer(submission)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                "error": f"Grok xato: {str(e)}",
                "debug": "API key tekshiring"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def submit_final(self, request, pk=None):
        submission = self.get_object()
        submission.submitted_at = timezone.now()
        submission.save()
        return Response({"message": "Submitted! Call /evaluate/ to score."})
    

