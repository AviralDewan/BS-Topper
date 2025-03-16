from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, Group, Permission

class StudentUser(AbstractUser):
    '''
    Model for storing student's information includes:
    - username, password, first name, last name, program, level, date joined, mobile number, bio, profile picture, roll number, email
    '''

    groups = models.ManyToManyField(Group, related_name="student_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="student_permissions", blank=True)

    PROGRAM_CHOICES = (
        ('DS', 'Data Science'),
        ('ES', 'Electronic Systems')
    )

    LEVEL_CHOICES = (
        ('FL', 'Foundation'),
        ('DP', 'Diploma'),
        ('DG', 'Degree')
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    program = models.CharField(max_length=25, choices=PROGRAM_CHOICES, blank=True, null=True)
    level = models.CharField(max_length=25, choices=LEVEL_CHOICES, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.URLField(blank=True, null=True)
    roll_number = models.CharField(max_length=10, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    mobile_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Invalid phone number")]
    )

    def __str__(self):
        return f"{self.id}: {self.username} by {self.first_name} {self.last_name}"
