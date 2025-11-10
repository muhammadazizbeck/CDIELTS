from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class WritingTask(models.Model):
    TASK_CHOICES = (
        ("task1","Task 1"),
        ("task2","Task 2")
    )
    task_type = models.CharField(max_length=10,choices=TASK_CHOICES)
    image = models.ImageField(upload_to='writing_images',null=True,blank=True)
    title = models.CharField(max_length=400)
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Writing-{self.title[:30]}"

class WritingSubmission(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='submissions')
    task = models.ForeignKey(WritingTask,on_delete=models.CASCADE,related_name='submissions')
    answer = models.TextField()
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True,null=True)
    submitted_at = models.DateTimeField(blank=True,null=True)

    def save(self,*args,**kwargs):
        if not self.end_time:
            self.end_time = self.start_time + timedelta(hours=1)

        super().save(*args,**kwargs)

    def is_time_over(self):
        return timezone.now()>self.end_time
    
    def __str__(self):
        return f"{self.user.username}-Writing Submission"

class WritingEvaluation(models.Model):
    submission = models.OneToOneField(WritingSubmission,on_delete=models.CASCADE,related_name='evaluation')

    score = models.FloatField(null=True,blank=True)
    coherence = models.FloatField(null=True,blank=True)
    grammar = models.FloatField(null=True,blank=True)
    vocabulary = models.FloatField(null=True,blank=True)
    response = models.FloatField(null=True,blank=True)
    feedback = models.TextField(null=True,blank=True)

    def __str__(self):
        return f"Evaluation for {self.submission.task.task_type}"

    

