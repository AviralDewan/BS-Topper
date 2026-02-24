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

    PROGRAM_CHOICES = [
        ('DS', 'Data Science'),
        ('ES', 'Electronic Systems')
    ]

    LEVEL_CHOICES = [
        ('FL', 'Foundation'),
        ('DP', 'Diploma'),
        ('DG', 'Degree')
    ]

    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    program = models.CharField(max_length=25, choices=PROGRAM_CHOICES, blank=True, null=True)
    level = models.CharField(max_length=25, choices=LEVEL_CHOICES, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.URLField(default="https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small_2x/default-avatar-icon-of-social-media-user-vector.jpg", blank=True, null=True)
    roll_number = models.CharField(max_length=10, unique=True, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Invalid phone number")]
    )

    def __str__(self):
        return f"{self.id}: {self.username} by {self.first_name} {self.last_name}"

class BootcampRegister(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    roll = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return f"{self.id}: {self.name} -> {self.roll}"

# class EventRegistration(models.Model):
#     EVENT_TYPE_CHOICES = [
#         ("DSA", "DSA"),
#         ("IDEA", "Ideathon"),
#         ("HACK", "Hackathon"),
#     ]

#     event_id = models.IntegerField()
#     event_type = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES)

#     name = models.CharField(max_length=100)

#     phone = models.CharField(
#         max_length=10,
#         validators=[RegexValidator(r'^\d{10}$', 'Phone must be 10 digits')]
#     )

#     email = models.EmailField()

#     is_team = models.BooleanField(default=False)

#     team_emails = models.JSONField(blank=True, null=True)  

#     track = models.CharField(
#         max_length=20,
#         blank=True,
#         null=True
#     )  

#     accepted_rules = models.BooleanField(default=False)

#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ("event_id", "email")

#     def __str__(self):
#         return f"{self.name} - {self.event_id}"

class EventSubmission(models.Model):
    # pass
    event_id = models.IntegerField()
    email = models.EmailField()

    submission_link = models.URLField()

    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event_id", "email")

    def __str__(self):
        return f"{self.email} - {self.event_id}"

class EventRegistration(models.Model):
    EVENT_TYPE_CHOICES = [
        ("Pen It Down", "Pen It Down"),
        ("Talent Showcase", "Talent Showcase"),
        ("From Your Lens", "From Your Lens"),
        ("Vaak – Yuddh", "Vaak – Yuddh")
    ]

    event_id = models.IntegerField()
    event_type = models.CharField(max_length=30, choices=EVENT_TYPE_CHOICES)

    name = models.CharField(max_length=100)

    phone = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Phone number must be 10 digits')]
    )

    email = models.EmailField()  

    accepted_rules = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event_id", "email")

    def __str__(self):
        return f"{self.name} - {self.event_type} : {self.email}"

