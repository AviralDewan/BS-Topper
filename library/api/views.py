from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from student_auth.models import StudentUser
from library.models import Resource, ResourceSection, Row
from .serializers import RowSerializer, ResourceSectionSerializer, ResourceSerializer
from .permissions import IsCreatorOrAdmin
from .pagination import ResourcePaginator

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_resource(request):

    try:
        
        student = request.user

        name = request.data.get("name")
        desc = request.data.get("desc")
        tag = request.data.get("tag")

        if not name or not tag:
            return Response({"message": "Please provide required information"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ResourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({"message": "Resource created"}, status=status.HTTP_201_CREATED)

        return Response({"error": serializer.errors}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": "An error ocucured, couldn't create resource"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["GET"])
def search_library(request):

    try:

        tag = request.query_params.get("tag")

        if tag:
            tag = tag.strip().capitalize()
            if tag not in [tag_code[0] for tag_code in Resource.TAG_CHOICES]:
                return Response({"message": "Tag not found"}, status=status.HTTP_400_BAD_REQUEST)
            resources = Resource.objects.filter(tag=tag)
        else:
            resources = Resource.objects.all()

        paginator = ResourcePaginator()
        paginated_resources = paginator.paginate_queryset(resources, request)
        serializer = ResourceSerializer(paginated_resources, many=True)

        return paginator.get_paginated_response(serializer.data)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["GET"])
def get_resource(request, resource_id):
    try:
        if not resource_id:
            return Response({"message": "Please provide a Resource ID"}, status=status.HTTP_400_BAD_REQUEST)
        resource = Resource.objects.filter(id=resource_id)
        if not resource:
            return Response({"message": "Resource Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ResourceSerializer(resource[0])

        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status.HTTP_503_SERVICE_FORBIDDEN)

@api_view(["GET"])
def view_library(request):

    try:
        
        resources = Resource.objects.all()

        paginator = ResourcePaginator()
        paginated_resources = paginator.paginate_queryset(resources, request)

        serializer = ResourceSerializer(paginated_resources, many=True)

        return paginator.get_paginated_response(serializer.data)
    
    except Exception as e:
        return Response({"error": "An error ocucured, couldn't get resources"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def edit_resource(request, resource_id):

    try:

        resource = Resource.objects.get(id=resource_id)
        student = request.user

        permission = IsCreatorOrAdmin()

        if not permission.has_object_permission(request, None, resource):
            return Response({"message": permission.message}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ResourceSerializer(resource, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Resource updated"}, status=status.HTTP_200_OK)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    except Resource.DoesNotExist:
        return Response({"message": "Resource Not Found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_resource(request, resource_id):

    try:
        
        if not Resource.objects.filter(id=resource_id).exists():
            return Response({"message": "Resource doesn\'t exist"}, status=status.HTTP_404_NOT_FOUND)
        
        resource = Resource.objects.get(id=resource_id)

        permission = IsCreatorOrAdmin()
        if not permission.has_object_permission(request, None, resource):
            return Response({"message": permission.message}, status=status.HTTP_403_FORBIDDEN)
        
        resource.delete()

        return Response({"message": "Resource Deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    except Exception as e:
        return Response({"error": "An error ocucured, couldn't delete resource"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_resources(request):

    try:

        student = request.user

        resources = Resource.objects.filter(created_by=student)

        paginator = ResourcePaginator()
        paginated_resources = paginator.paginate_queryset(resources, request)

        serializer = ResourceSerializer(paginated_resources, many=True)

        return paginator.get_paginated_response(serializer.data)

    except Exception as e:
        return Response({"error": "An error ocucured, couldn't get your resources"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_resource_section(request, resource_id):

    try:
        
        student = request.user

        name = request.data.get("name")

        if not name:
            return Response({"message": "Please provide required information"}, status=status.HTTP_400_BAD_REQUEST)
        
        resource = Resource.objects.get(id=resource_id)

        if ResourceSection.objects.filter(name=name, resource=resource).exists():
            return Response({"message": "Resource Section with this name already exists under selected resource"}, status=status.HTTP_400_BAD_REQUEST)
        
        resource_section = ResourceSection.objects.create(name=name.strip(), created_by=student, resource=resource)

        return Response({"message": "Resource Section created"}, status=status.HTTP_201_CREATED)

    except Resource.DoesNotExist:
        return Response({"message": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({"error": "An error ocucured, couldn't create resource section"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def edit_resource_section(request, resource_section_id):

    try:
        
        if "resource_id" not in request.data:
            return Response({"message": "Please provie the required information"}, status=status.HTTP_400_BAD_REQUEST)

        resource_id = request.data["resource_id"]
        resource = Resource.objects.get(id=resource_id)
        student = request.user

        if "name" not in request.data and "desc" not in request.data:
                return Response({"message": "Please provie the required information"}, status=status.HTTP_400_BAD_REQUEST)

        if "name" in request.data:
            name = request.data["name"].strip()
        if "desc" in request.data:
            desc = request.data["desc"].strip()

        if ResourceSection.objects.filter(resource=resource,name=name).exclude(id=resource_section_id).exists():
            return Response({"message": "A resource section with same name exists under this resource exists, please provide a different name"}, status=status.HTTP_400_BAD_REQUEST)

        resource_section = ResourceSection.objects.get(id=resource_section_id)

        permission = IsCreatorOrAdmin()
        if not resource.created_by == student and not permission.has_object_permission(request, None, resource_section):
            return Response({"message": permission.message}, status=status.HTTP_403_FORBIDDEN)

        serializer = ResourceSectionSerializer(resource_section, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Resource Section updated"}, status=status.HTTP_200_OK)

        return Response({"message": "Couldn't update resource section"}, status=status.HTTP_400_BAD_REQUEST)
    
    except Resource.DoesNotExist:
        return Response({"message": "Resource Not Found"}, status=status.HTTP_404_NOT_FOUND)
    except ResourceSection.DoesNotExist:
        return Response({"message": "Resource Section Not Found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": "An error ocucured, couldn't update resource section"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_resource_section(request, resource_section_id):

    try:
        
        if "resource_id" not in request.data:
            return Response({"message": "Please provide the required information"}, status=status.HTTP_400_BAD_REQUEST)

        resource_id = request.data["resource_id"]
        resource = Resource.objects.get(id=resource_id)
        resource_section = ResourceSection.objects.get(id=resource_section_id, resource=resource)
        student = request.user

        permission = IsCreatorOrAdmin()
        if not resource.created_by == student and not permission.has_object_permission(request, None, resource_section):
            return Response({"message": permission.message}, status=status.HTTP_403_FORBIDDEN)
        
        resource_section.delete()

        return Response({"message": "Resource Section Deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    except Resource.DoesNotExist:
        return Response({"message": "Resource Not Found"}, status=status.HTTP_404_NOT_FOUND)
    except ResourceSection.DoesNotExist:
        return Response({"message": "Resource Section Not Found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": "An error occured, couldn't delete resource section"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_row(request, resource_section_id):
    try:
        name = request.data.get('name')
        link = request.data.get('link')

        if not name or not link:
            return Response({"message": "Please provide required information"}, status=status.HTTP_400_BAD_REQUEST)

        resource_section = ResourceSection.objects.get(id=resource_section_id)

        serializer = RowSerializer(
            data=request.data,
            context={"resource_section": resource_section, "student": request.user}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Row created"}, status=status.HTTP_201_CREATED)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except ResourceSection.DoesNotExist:
        return Response({"error": "Resource Section Not Found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": "An error occurred, couldn't add row"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def edit_row(request, resource_section_id, row_id):

    try:

        resource_section = ResourceSection.objects.get(id=resource_section_id)
        student = request.user

        if "name" not in request.data and "link" not in request.data and "desc" not in request.data:
                return Response({"message": "Please provie the required information"}, status=status.HTTP_400_BAD_REQUEST)

        row = Row.objects.get(id=row_id)

        permission = IsCreatorOrAdmin()

        if not resource_section.resource.created_by == student and not resource_section.created_by == student and not permission.has_object_permission(request, None, row):
            return Response({"message": permission.message}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = RowSerializer(row, data=request.data, context={"resource_section": resource_section}, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Row updated"}, status=status.HTTP_200_OK)
        
        return Response({"message": serializer.errors}, status=status.HTTP_200_OK)
    
    except ResourceSection.DoesNotExist:
        return Response({"error": "Resource Section Not Found"}, status=status.HTTP_404_NOT_FOUND)
    except Row.DoesNotExist:
        return Response({"error": "Row Not Found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_row(request, row_id):

    try:
        
        row = Row.objects.get(id=row_id)
        student = request.user.id

        permission = IsCreatorOrAdmin()

        if not row.resource_section.created_by == student and not row.resource_section.resource.created_by == student and not permission.has_object_permission(request, None, row):
            return Response({"error": permission.message}, status=status.HTTP_403_FORBIDDEN)
        
        row.delete()

        return Response({"error": "Row Deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    except Row.DoesNotExist:
        return Response({"error": "Row Not Found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": "An error occured, couldn't delete row"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

def get_sections(request, resource_id):

    if request.method == 'GET':
        
        if not Resource.objects.filter(id=resource_id).exists():
            return HttpResponse('Resource doesn\'t exist')
        
        resource = Resource.objects.get(id=resource_id)

        data = {}
        data['intro'] = {
            'name': resource.name,
            'desc': resource.desc,
            'tag': resource.tag,
            'created_by': resource.created_by.username,
            'created_on': resource.created_on
        }
        for section in ResourceSection.objects.filter(resource=resource):
            section_data = {}
            section_data['name'] = section.name
            section_data['created_by'] = section.created_by.username
            section_data['created_on'] = section.created_on

            row_data = {}
            for row in Row.objects.filter(resource_section=section):
                row_data[row.id] = {
                    'name': row.name,
                    'link': row.link,
                    'created_by': row.created_by.username,
                    'created_on': row.created_on
                }
            
            data[section.id] = {
                'section_info': section_data,
                'rows': row_data
            }

        return JsonResponse(data)
    
    return HttpResponse('Incorrect REST method') 


