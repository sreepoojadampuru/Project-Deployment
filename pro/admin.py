from django.contrib import admin
from .models import Task, CodeSnippet, Student

admin.site.register(Task)
admin.site.register(CodeSnippet)
admin.site.register(Student)
