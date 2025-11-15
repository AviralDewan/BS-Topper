from django.db import models
from student_auth.models import StudentUser

class NewsLetter(models.Model):
    email = models.EmailField(unique=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.email}"

class Todo(models.Model):
    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE, related_name="todos")
    todo = models.CharField(max_length=150, null=False, blank=True)
    checked = models.BooleanField(default=False)
    addedOn = models.DateTimeField(auto_now_add=True)
    completedOn = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}: {self.todo} by {self.student.username}"
