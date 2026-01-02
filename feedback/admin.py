from django.contrib import admin
from feedback.models import ClassFeedback, Feedback

# Register your models here.

admin.site.register(ClassFeedback)
admin.site.register(Feedback)
