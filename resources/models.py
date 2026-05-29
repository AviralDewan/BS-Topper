from django.db import models
from student_auth.models import Student

class Resource(models.Model):

    TAG_CHOICES = [
    ("Institute", "Institute"),
    ("Academic", "Academic"),
    ("PYQs", "PYQs"),
    ("Placements", "Placements"),
    ("Internships", "Internships"),
    ("Paradox(Fest)", "Paradox(Fest)"),
    ("Books", "Books"),
    ("Other", "Other")
  ]

    creator = models.ForeignKey(Student, on_delete=models.SET_NULL, related_name="resources", null=True)
    created_on = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=800, null=True)
    url = models.URLField(null=True)
    tag = models.CharField(max_length=50, choices=TAG_CHOICES, blank=True)

    def __str__(self):
        user = None
        if self.creator:
            user = self.creator.username
        return f"{self.id}: {self.title} by {user}"

