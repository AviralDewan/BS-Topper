from django.urls import path
from . import views

app_name = 'contest_event'
urlpatterns = [
    path('get-contest/', views.get_contest, name='get_contest'),
    path('get-event/', views.get_event, name='get_event')
]