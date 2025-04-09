from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('view-library/', views.view_library, name='view_library'),
    path('search-library/<str:tag>/', views.search_library, name='search_library'),
    path('add-resource/', views.add_resource, name='add_resource'),
    path('edit-resource/<int:resource_id>/', views.edit_resource, name='edit_resource'),
    path('delete-resource/<int:resource_id>/', views.delete_resource, name='delete_resource'),
    path('get-my-resources/', views.get_my_resources, name='get_my_resources'),
    path('add-resource-section/<int:resource_id>/', views.add_resource_section, name='add_resource_section'),
    path('edit-resource_section/<int:resource_section_id>/', views.edit_resource_section, name='edit_resource_section'),
    path('delete-resource_section/<int:resource_section_id>/', views.delete_resource_section, name='delete_resource_section'),
    path('add-row/<int:resource_section_id>/', views.add_row, name='add_row'),
    path('edit-row/<int:resource_section_id>/<int:row_id>/', views.edit_row, name='edit_row'),
    path('delete-row/<int:row_id>/', views.delete_row, name='delete_row')
]