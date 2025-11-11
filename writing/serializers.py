# backend/writing/serializers.py
from rest_framework import serializers
from .models import WritingTask, WritingSubmission

class WritingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = WritingTask
        fields = '__all__'

class WritingSubmissionSerializer(serializers.ModelSerializer):
    task = WritingTaskSerializer(read_only=True)
    task_id = serializers.IntegerField(write_only=True)
    evaluation = serializers.SerializerMethodField()

    class Meta:
        model = WritingSubmission
        fields = ['id', 'task', 'task_id', 'answer', 'evaluation']

    def get_evaluation(self, obj):
        try:
            return {
                "score": obj.eval.score,
                "coherence": obj.eval.coherence,
                "grammar": obj.eval.grammar,
                "vocabulary": obj.eval.vocabulary,
                "response": obj.eval.response,
                "feedback": obj.eval.feedback
            }
        except:
            return None

    # create() ni oddiy qilamiz - faqat saqlaymiz
    def create(self, validated_data):
        return WritingSubmission.objects.create(**validated_data)

    
