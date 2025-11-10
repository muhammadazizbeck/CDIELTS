from django.contrib import admin
from writing.models import WritingTask,WritingEvaluation,WritingSubmission

# Register your models here.

admin.site.register(WritingTask)
admin.site.register(WritingEvaluation)
admin.site.register(WritingSubmission)
