from django.db import models
from student_auth.models import StudentUser
from lectures.models import Lecture

class Flashcard(models.Model):
    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE, related_name="flashcards")
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name="flashcards")
    question = models.CharField(max_length=100, blank=False, null=False)
    answer = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"{self.id}: Lec - {self.lecture.id} by {self.student.id}"
