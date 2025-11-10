from rest_framework import serializers
from writing.models import WritingCheck

class WritingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = WritingCheck
        fields = "__all__"
        read_only_fields = (
            'user','title',"image",'score',"coherence",
            'grammer','vocabulary','response','feedback',
            "created_at",'updated_at',
            )