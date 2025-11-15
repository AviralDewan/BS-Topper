from django.contrib import admin
from .models import StudentUser, BootcampRegister

# Register your models here.
admin.site.register(StudentUser)
admin.site.register(BootcampRegister)