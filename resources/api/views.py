from django.shortcuts import render
from .serializers import ResourceSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCreator
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, CreateAPIView
from resources.models import Resource

class ResourceCreateView(CreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class ResourceCRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Resource
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated, IsCreator]
    http_method_names = ["get", "patch", "delete"]

class ResourceDetailView(RetrieveAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

class ResourceListView(ListAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
