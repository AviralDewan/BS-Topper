from django.urls import path
from .views import ResourceCRUDView, ResourceDetailView, ResourceListView, ResourceCreateView

urlpatterns = [
    path("crud/<int:pk>/", ResourceCRUDView.as_view(), name="crud_resources"),
    path("create/", ResourceCreateView.as_view(), name="create_resource"),
    path("<int:pk>/", ResourceDetailView.as_view(), name="single_resource"),
    path("list/", ResourceListView.as_view(), name="list_resources")
]