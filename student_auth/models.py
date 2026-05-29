from django.db import models
from django.contrib.auth.models import AbstractUser

class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Student(AbstractUser):
    PROGRAM_CHOICES = [
        ("Data Science", "Data Science"),
        ("Electronic Systems", "Electronic Systems"),
        ("Management", "Management"),
        ("Aerospace", "Aerospace")
    ]
    LEVEL_CHOICES = [
        ("Foundation", "Foundation"),
        ("Diploma", "Diploma"),
        ("Degree", "Degree")
    ]

    skills = models.ManyToManyField(Skill, related_name="students", blank=True)
    program = models.CharField(max_length=50, choices=PROGRAM_CHOICES, blank=True)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, blank=True)

    def __str__(self):
        return f"{self.id}: {self.username}"
