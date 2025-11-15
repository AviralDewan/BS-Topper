from django.urls import path
from . import views

app_name = 'student_profile'
urlpatterns = [
    path('get-profile-details/<int:pk>/', views.get_profile_details, name='get_profile_details'),
    path('edit-profile-details/', views.edit_profile_details, name='edit_profile_details'),
    path('add_to_newsletter', views.add_to_newsletter, name="add_to_newsletter"),
    path('add-todo', views.add_todo, name="add_todo"),
    path('get-todo', views.get_todo, name="get_todo"),
    path('update-todo', views.update_todo, name="update_todo"),
    path('delete-todo', views.delete_todo, name="delete_todo"),
]