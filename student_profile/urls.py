from django.urls import path
from . import views

app_name = 'student_profile'
urlpatterns = [
    path('get-profile-details/<int:student_id>/', views.get_profile_details, name='get_profile_details'),
    path('edit-profile-details/', views.edit_profile_details, name='edit_profile_details')
]