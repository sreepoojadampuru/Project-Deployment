from django.db import models
from django.contrib.auth.models import User




# Model to store tasks or notes
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Model to store executed code snippets
class CodeSnippet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='code_snippets')
    language = models.CharField(max_length=50)
    code = models.TextField()
    output = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.language} snippet by {self.user.username}"

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()

    def str(self):
        return self.name






