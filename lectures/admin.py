from django.contrib import admin
from .models import Course, Lecture, TimeStamp

admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(TimeStamp)
