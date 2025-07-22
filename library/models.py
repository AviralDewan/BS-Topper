from django.db import models
from student_auth.models import StudentUser

class Resource(models.Model):

    def update_admin():
        return StudentUser.objects.get(username="admin")
    
    TAG_CHOICES = [
        ("Institute", "Institute"),
        ("Academic", "Academic"),
        ("PYQs", "PYQs"),
        ("Placements", "Placements"),
        ("Internships", "Internships"),
        ("Paradox(Fest)", "Paradox(Fest)"),
        ("Books", "Books"),
        ("Misc", "Misc")
    ]
    EXAM_TYPE_CHOICES = [
        ("Quiz 1", "Quiz 1"),
        ("Quiz 2", "Quiz 2"),
        ("End Term", "End Term")
    ]
    EXAM_SESSION_CHOICES = [
        ("Morning", "Morning"),
        ("Afternoon", "Afternoon")
    ]
    SUBJECT_CHOICES = [
        ("English 1", "English 1"),
        ("English 2", "English 2"),
        ("Python", "Python"),
        ("Maths 1", "Maths 1"),
        ("Maths 2", "Maths 2"),
        ("Stats 1", "Stats 1"),
        ("Stats 2", "Stats 2"),
        ("CT", "CT"),
    ]

    name = models.CharField(max_length=255, unique=True)
    desc = models.TextField(null=True, blank=True)
    is_pyq = models.BooleanField(default=False, null=True)
    subject = models.CharField(max_length=100, choices=SUBJECT_CHOICES, null=True, blank=True)
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES, null=True, blank=True)
    tag = models.CharField(max_length=20, choices=TAG_CHOICES)
    held_on = models.DateField(null=True, blank=True)
    session = models.CharField(max_length=15, choices=EXAM_SESSION_CHOICES, null=True, blank=True)
    link = models.URLField(default="")
    created_by = models.ForeignKey(StudentUser, on_delete=models.SET(update_admin), related_name="resources")
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: {self.name} by {self.created_by.username}"
    
class ResourceSection(models.Model):

    def update_admin():
        return StudentUser.objects.get(username="admin")

    name = models.CharField(max_length=100)
    desc = models.TextField(max_length=100, blank=True)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="sections")
    created_by = models.ForeignKey(StudentUser, on_delete=models.SET(update_admin), related_name="sections")
    created_on = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("name", "resource")

    def __str__(self):
        return f"{self.id}: {self.resource.name}/{self.name}"
    
class Row(models.Model):
    
    def update_admin():
        return StudentUser.objects.get(username="admin")
    
    name = models.CharField(max_length=100)
    link = models.URLField()
    desc = models.CharField(max_length=100, blank=True)
    resource_section = models.ForeignKey(ResourceSection, on_delete=models.CASCADE, related_name="rows")
    created_by = models.ForeignKey(StudentUser, on_delete=models.SET(update_admin), related_name="rows")
    created_on = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = [("name", "resource_section"), ("link", "resource_section")]

    def __str__(self):
        return f"{self.id}: {self.resource_section.resource.name}/{self.resource_section.name}/{self.name}"
