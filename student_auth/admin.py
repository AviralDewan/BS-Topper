from django.contrib import admin
from .models import StudentUser, BootcampRegister, EventRegistration, EventSubmission

# Register your models here.
admin.site.register(StudentUser)
admin.site.register(BootcampRegister)
admin.site.register(EventRegistration)
admin.site.register(EventSubmission)
