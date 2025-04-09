from django.db import models
from student_auth.models import StudentUser

class Resource(models.Model):

    def update_admin():
        return StudentUser.objects.get(username="admin")
    
    TAG_CHOICES = [
        ("College", "College"),
        ("Fun", "Fun"),
        ("Win", "Win"),
    ]

    name = models.CharField(max_length=255, unique=True)
    desc = models.TextField()
    tag = models.CharField(max_length=20, choices=TAG_CHOICES)
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
