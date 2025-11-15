from django.urls import path
from . import views

app_name = 'flashcards'
urlpatterns = [
    path("get-or-create/<int:lecture_id>", views.get_or_create_flashcard, name="get_or_create_flashcard"),
    path("get/<int:fc_id>", views.get_flashcard, name="get_flashcard"),
    path("delete/<int:fc_id>", views.delete_flashcard, name="delete_flashcard"),
    path("update/<int:fc_id>", views.update_flashcard, name="update_flashcard"),
    path("get-all", views.get_all, name="get_all"),
    path("get-my-flashcards", views.get_my_flashcards, name="get_my_flashcards")
]
