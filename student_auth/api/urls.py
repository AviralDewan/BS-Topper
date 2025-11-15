from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = 'student_auth'
urlpatterns = [
    path('register/', views.register_student, name='register_student'),
    path('signup/', views.signup, name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh_token')
]
