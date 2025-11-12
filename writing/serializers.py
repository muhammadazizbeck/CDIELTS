# backend/writing/serializers.py
from rest_framework import serializers
from .models import WritingTask, WritingSubmission, WritingEvaluation

class WritingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = WritingTask
        fields = ['id', 'task_type', 'title', 'question', 'image']

class WritingEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WritingEvaluation
        fields = ['score', 'coherence', 'grammar', 'vocabulary', 'response', 'feedback']

class WritingSubmissionSerializer(serializers.ModelSerializer):
    task = WritingTaskSerializer(read_only=True)
    evaluation = WritingEvaluationSerializer(read_only=True)

    class Meta:
        model = WritingSubmission
        fields = ['id', 'task', 'answer', 'start_time', 'end_time', 'evaluation']

    
