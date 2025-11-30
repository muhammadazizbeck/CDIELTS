from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class WritingTask1(models.Model):
    image = models.ImageField(upload_to='writings/images')
    title = models.CharField(max_length=250)
    question = models.CharField(max_length=300)
    recommended_minutes = models.PositiveSmallIntegerField(default=20, help_text="Tavsiya etilgan vaqt (daqiqa)")

    def __str__(self):
        return self.title[:120]
    
class WritingTask2(models.Model):
    title = models.CharField(max_length=250)
    question = models.CharField(max_length=300)
    recommended_minutes = models.PositiveSmallIntegerField(default=40, help_text="Tavsiya etilgan vaqt (daqiqa)")

    def __str__(self):
        return self.title[:120]


    

    


    

