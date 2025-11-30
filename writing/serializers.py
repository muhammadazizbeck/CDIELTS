# backend/writing/serializers.py
from rest_framework import serializers
from .models import WritingTask1,WritingTask2

class WritingTask1Serializer(serializers.ModelSerializer):
    class Meta:
        model = WritingTask1
        fields = ["image","title","question","recommended_minutes"]


class WritingTask2Serializer(serializers.ModelSerializer):
    class Meta:
        model = WritingTask2
        fields = ['title','question','recommended_minutes']
    



    
