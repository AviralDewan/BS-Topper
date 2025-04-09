from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from student_auth.models import StudentUser

class Course(models.Model):
    '''
     Model for storing course information includes:
     - course name, course offered in program, course offered at level
    '''

    PROGRAM_CHOICES = (
        ('DS', 'Data Science'),
        ('ES', 'Electronic Systems')
    )

    LEVEL_CHOICES = (
        ('FL', 'Foundation'),
        ('DP', 'Diploma'),
        ('DG', 'Degree')
    )

    name = models.CharField(max_length=255)
    program = models.CharField(max_length=20, choices=PROGRAM_CHOICES)
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES)
    weeks = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(15)])

    def __str__(self):
        return f"{self.id}: {self.name} offered in {self.program} at {self.level} level"

class Lecture(models.Model):
    '''
     Model for storing lecture information includes:
     - lecture name, lecture number, week name, course associated with, video link, duration
    '''

    name = models.CharField(max_length=255)
    lecture_number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(15)])
    week_name = models.CharField(max_length=30)
    week_number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(15)])
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lecture')
    video_link = models.URLField()
    duration = models.FloatField()

    def __str__(self):
        return f"{self.id}: {self.name} - {self.course.name}"

class TimeStamp(models.Model):
    '''
    Model for storing user's timestamp on lectures, includes:
    - start and end timestamps, lecture reference, student reference
    '''
    name = models.CharField(max_length=50)
    start_timestamp = models.TimeField()
    end_timestamp = models.TimeField(blank=True, null=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='time_stamps')
    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE, related_name='time_stamps')

    def __str__(self):
        return f"{self.id}: {self.start_timestamp} - {self.end_timestamp} on {self.lecture.name}"
