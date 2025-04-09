from django.urls import path
from . import views

app_name = 'groups'
urlpatterns = [
    path('create-group/', views.create_group, name='create_group'),
    path('edit-group/', views.edit_group, name='edit_group'),
    path('change-admin/', views.change_admin, name='change_admin'),
    path('join-group/', views.join_group, name='join-group'),
    path('leave-group/', views.leave_group, name='leave_group'),
    path('get-my-groups/', views.get_my_groups, name='get_my_groups'),
    path('make-post/', views.make_post, name='make_post'),
    path('get-my-posts/', views.get_my_posts, name='get_my_posts'),
    path('view-posts/<int:group_id>/', views.view_posts, name='view_posts'),
    path('view-post/<int:post_id>/', views.view_post, name='view_post'),
    path('delete-post/<int:post_id>/', views.delete_post, name='post_id'),
    path('get-pinned-post/<int:group_id>/', views.get_pinned_post, name='get_pinned_post'),
    path('set-pinned-post/<int:group_id>/', views.set_pinned_post, name='set_pinned_post'),
    path('post-comment/<int:post_id>/', views.post_comment, name='post_comment'),
    path('delete-comment/<int:post_id>/', views.delete_comment, name='delete_comment'),
    path('toggle-vote/<int:post_id>/', views.toggle_vote, name='toggle_vote')
]