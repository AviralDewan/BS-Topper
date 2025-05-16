from django.urls import path
from . import views

app_name = 'lectures'
urlpatterns = [
    path('get-current-program-level-details/', views.get_current_program_level_details, name='get_current_program_level_details'),
    path('get-course-list/', views.get_course_list, name='get_course_list'),
    path('get-test-fields/', views.get_test_fields, name='get_test_fields'),
    path('calc-score/', views.calc_score, name='calc_score'),
    path('get-weeks-and-lectures/<int:course_id>/', views.get_weeks_and_lectures, name='get_weeks_and_lectures'),
    path('get-timestamps/', views.get_timestamps, name='get_timestamps'),
    path('save-timestamps/', views.save_timestamps, name='save_timestamps'),
    path('delete-timestamps/<int:timestamp_id>/', views.delete_timestamps, name='delete_timestamps'),
    # path('ai-help', views.ai_help, name='ai_help')
]