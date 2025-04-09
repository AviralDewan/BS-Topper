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

        if not name or not desc or not tag:
            return Response({"message": "Please provide required information"}, status=status.HTTP_400_BAD_REQUEST)
        
        if tag not in [tag[0] for tag in Resource.TAG_CHOICES]:
            return Response({"message": "Tag not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        if Resource.objects.filter(name=name).exists():
            return Response({"message": "Resource already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        resource = Resource.objects.create(name=name.strip(),desc=desc.strip(),tag=tag,created_by=student)

        return Response({"message": "Resource created"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": "An error ocucured, couldn't create resource"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

def search_library(request, tag):

    if request.method == 'GET':

        if tag not in [tag_code[0] for tag_code in Resource.TAG_CHOICES]:
            return HttpResponse('Tag not found')
        
        resources = Resource.objects.filter(tag=tag)

        data = {
            resource.id: {
                'name': resource.name,
                'desc': resource.desc,
                'created_on': resource.created_on,
                'created_by': resource.created_by.username
            }
            for resource in resources
        }

        return JsonResponse(data)
    
    return HttpResponse('Incorrect REST method')

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

def edit_resource(request, resource_id):

    if request.method == 'PUT':
        
        if not request.user.is_authenticated:
            return HttpResponse('You must be logged in to perform this action')
        
        if not Resource.objects.filter(id=resource_id).exists():
            return HttpResponse('Resource doesn\'t exist')
        
        data = json.loads(request.body)

        resource = Resource.objects.get(id=resource_id)
        student = StudentUser.objects.get(id=request.user.id)

        if resource.created_by != student:
            return HttpResponse('You don\'t have required permission')

        if 'name' in data:
            if Resource.objects.filter(name=data['name'].strip()).exists():
                return HttpResponse('A resource with same name exists, please provide a different name')
            resource.name = data['name'].strip()
        if 'desc' in data:
            resource.desc = data['desc'].strip()
        if 'tag' in data:
            if not data['tag'].strip() in [tag_code[0] for tag_code in Resource.TAG_CHOICES]:
                return HttpResponse('Provided tag doesn\'t exist, please provide a different tag')
            resource.tag = data['tag'].strip()
        
        resource.save()

        return HttpResponse('Resource updated')
    
    return HttpResponse('Incorrect REST method')

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
        
        if not request.user.is_authenticated:
            return HttpResponse('You must be logged in to perform this action')
        
        if not Resource.objects.filter(id=resource_id).exists():
            return HttpResponse('Resource doesn\'t exist')
        
        data = json.loads(request.body)

        resource = Resource.objects.get(id=resource_id)
        student = StudentUser.objects.get(id=request.user.id)

        if not ResourceSection.objects.filter(id=resource_section_id).exists():
            return HttpResponse('Resource Section doesn\'t exist')

        if 'name' not in data:
                return HttpResponse('Please provie the required information')

        if ResourceSection.objects.filter(resource=resource,name=data['name'].strip()).exists():
            return HttpResponse('A resource section with same name exists under this resource, please provide a different name')

        resource_section = ResourceSection.objects.get(id=resource_section_id)
        print(resource_section)

        if resource_section.created_by != student:
            return HttpResponse('You don\'t have required permission')

        resource_section.name = data['name'].strip()
        resource_section.save()

        return HttpResponse('Resource Section updated')
    
    except Exception as e:
        return Response({"error": "An error ocucured, couldn't create resource section"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

def delete_resource_section(request, resource_section_id):

    if request.method == 'DELETE':

        if not request.user.is_authenticated:
            return HttpResponse('You must be logged in to perform this action')
        
        if not Resource.objects.filter(id=resource_id).exists():
            return HttpResponse('Resource doesn\'t exist')
        
        if not ResourceSection.objects.filter(id=resource_section_id).exists():
            return HttpResponse('Resource Sectoin doesn\'t exist')
        
        resource = Resource.objects.get(id=resource_id)
        resource_section = ResourceSection.objects.get(id=resource_section_id)
        student = StudentUser.objects.get(id=request.user.id)

        if resource.created_by != student and resource_section.created_by != student and student.username != 'admin':
            return HttpResponse('You don\'t have required permission')
        
        resource_section.delete()

        return HttpResponse('Resource Section Deleted')
    
    return HttpResponse('Incorrect REST method')    

def add_row(request, resource_section_id):

    if request.method == 'POST':

        if not request.user.is_authenticated:
            return HttpResponse('You must be logged in to perform this action')
        
        student = StudentUser.objects.get(id=request.user.id)

        name = request.POST.get('name')
        link = request.POST.get('link')

        if not name or not link:
            return HttpResponse('Please provide required information')
        
        if not ResourceSection.objects.filter(id=resource_section_id).exists():
            return HttpResponse('Resource Section doesn\'t exist')
        
        resource_section = ResourceSection.objects.get(id=resource_section_id)

        if Row.objects.filter(link=link, resource_section=resource_section).exists():
            return HttpResponse('A row with this link already exists under this resource section')
        
        row = Row.objects.create(name=name.strip(), link=link.strip(), created_by=student, resource_section=resource_section)

        return HttpResponse('Row created')

    return HttpResponse('Incorrect REST method')

def edit_row(request, resource_section_id, row_id):

    if request.method == 'PUT':
        
        if not request.user.is_authenticated:
            return HttpResponse('You must be logged in to perform this action')
        
        if not ResourceSection.objects.filter(id=resource_section_id).exists():
            return HttpResponse('Resource Section doesn\'t exist')
        
        data = json.loads(request.body)

        resource_section = ResourceSection.objects.get(id=resource_section_id)
        student = StudentUser.objects.get(id=request.user.id)

        if 'name' not in data and 'link' not in data:
                return HttpResponse('Please provie the required information')

        if Row.objects.filter(resource_section=resource_section,link=data['link'].strip()).exists():
            return HttpResponse('A row with same link already exists under this resource section')

        row = Row.objects.get(id=row_id)

        if row.created_by != student and student.username != 'admin' and student != resource_section.resource.created_by and student != resource_section.created_by:
            return HttpResponse('You don\'t have required permission')

        if 'name' in data:
            row.name = data['name'].strip()
        if 'link' in data:
            row.link = data['link'].strip()
        
        row.save()

        return HttpResponse('Row updated')
    
    return HttpResponse('Incorrect REST method')

def delete_row(request, row_id):

    if request.method == 'DELETE':

        if not request.user.is_authenticated:
            return HttpResponse('You must be logged in to perform this action')
        
        if not Row.objects.filter(id=row_id).exists():
            return HttpResponse('Row doesn\'t exist')
        
        row = Row.objects.get(id=row_id)
        student = StudentUser.objects.get(id=request.user.id)

        if row.created_by != student and row.resource_section.created_by != student and student.username != 'admin' and row.resource_section.resource.created_by != student:
            return HttpResponse('You don\'t have required permission')
        
        row.delete()

        return HttpResponse('Row Deleted')
    
    return HttpResponse('Incorrect REST method')    

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


