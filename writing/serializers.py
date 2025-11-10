from rest_framework import serializers
from writing.models import WritingTask,WritingSubmission,WritingEvaluation

class WritingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = WritingTask
        fields = "__all__"
        read_only_fields = ("task_type","image","title","question")

    
