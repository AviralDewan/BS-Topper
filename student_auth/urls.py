from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = 'student_auth'
urlpatterns = [
    path('sign-up/', views.signup_student, name='signup_student'),
    path('login/', views.login_student, name='login_student'),
    path('logout/', views.logout_student, name='logout_student')
    # path('login/', TokenObtainPairView.as_view(), name='login'),
    # path('refresh-token/', TokenRefreshView, name='refresh-token')
]
