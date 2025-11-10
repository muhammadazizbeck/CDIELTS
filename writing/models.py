from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class WritingCheck(models.Model):
    TASK_CHOICES = (
        ('task1',"Task1"),
        ("task2",'Task2')
    )
    
    task_type = models.CharField(max_length=10,choices=TASK_CHOICES)
    title = models.TextField()
    image = models.ImageField(upload_to='writing_images/',null=True,blank=True)

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='writing_tasks')
    text = models.TextField(null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    score = models.FloatField(null=True,blank=True)
    coherence = models.FloatField(null=True,blank=True)
    grammar = models.FloatField(null=True,blank=True)
    vocabulary = models.FloatField(null=True,blank=True)
    response = models.FloatField(null=True,blank=True)
    feedback = models.TextField(null=True,blank=True)

    def __str__(self):
        return f"{self.user.username}-{self.task_type}-{self.title}"
    

