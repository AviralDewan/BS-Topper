import json
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.db.models import Count
from student_auth.models import StudentUser
from .models import Group, GroupMembership, Post, PinnedPost, Comment, PostVotes

def create_group(request):
    if request.method == 'POST':

        if not request.user.is_authenticated:
            return HttpResponse('Only logged in users can create groups')

        name = request.POST.get('group_name')
        desc = request.POST.get('desc')
        rules = request.POST.get('rules')
        profile_pic = request.POST.get('profile_pic')

        if not name or not desc or not rules or not profile_pic:
            return HttpResponse('Please provide required information')
        
        student = StudentUser.objects.get(id=request.user.id)

        if student.username != 'admin' and Group.objects.filter(admin=student).exists():
            return HttpResponse('You can be admin of only 1 group at a time')

        if Group.objects.filter(name=name).exists():
            return HttpResponse('Group with same name already exits, please enter a different name')

        group = Group.objects.create(admin=student, name=name.strip(), desc=desc.strip(), rules=rules.strip(), profile_pic=profile_pic.strip())

        return HttpResponse('Group created')

    return HttpResponse('Incorrect REST method')

def edit_group(request):
    if request.method == 'PUT':

        if not request.user.is_authenticated:
            return HttpResponse('To edit the group info, please login')

        group_data = json.loads(request.body)
        group_id = group_data.get('group_id')

        if not Group.objects.filter(id=group_id).exists():
            return HttpResponse('Group doesn\'t exist')
        
        student = StudentUser.objects.get(id=request.user.id)
        print(Group.objects.get(id=group_id).admin == student)

        if not Group.objects.get(id=group_id).admin == student and not Group.objects.get(id=group_id).admin == StudentUser.objects.get(username='admin'):
            return HttpResponse('You do not have the required permission')

        group = Group.objects.get(id=group_id)

        info_provided = False
        if 'name' in group_data:
            if Group.objects.filter(name=group_data['name']).exists():
                return HttpResponse('Group with same name already exists, please choose a different name')
            group.name = group_data['name'].strip()
            info_provided = True
        if 'desc' in group_data:
            group.desc = group_data['desc'].strip()
            info_provided = True
        if 'rules' in group_data:
            group.rules = group_data['rules'].strip()
            info_provided = True
        if 'profile_pic' in group_data:
            group.profile_pic = group_data['profile_pic']
            info_provided = True
        if not info_provided:
            return HttpResponse('Please provide information to be updated')

        group.save()

        return HttpResponse('Group info updated')
    
    return HttpResponse('Incorrect REST method')

def change_admin(request):
    if request.method == 'PUT':

        if not request.user.is_authenticated:
            return HttpResponse('You must be logged in to perform this action')
        
        current_admin_id = request.user.id
        data = json.loads(request.body)

        if 'new_admin_id' not in data:
            return HttpResponse('Please select the new admin')

        new_admin_id = data.get('new_admin_id')

        if not StudentUser.objects.filter(id=new_admin_id).exists():
            return HttpResponse('User with provided ID doesn\'t exist')

        current_admin = StudentUser.objects.get(id=current_admin_id)

        if not Group.objects.filter(admin=current_admin).exists():
            return HttpResponse('You must be an admin to perform this action')

        new_admin = StudentUser.objects.get(id=new_admin_id)
        if new_admin.username == 'admin':
            return HttpResponse('You cannot perform this action')

        group = Group.objects.get(admin=current_admin)

        if group.admin != current_admin:
            return HttpResponse('You don\'t have the required permission to perform this action')
        
        if not GroupMembership.objects.filter(student=new_admin).exists():
            return HttpResponse('Only group members can become admin')

        group.admin = new_admin
        group.save()

        return HttpResponse('Group admin updated')

    return HttpResponse('Incorrect REST method')

def join_group(request):
    if request.method == 'POST':

        if not request.user.is_authenticated:
            return HttpResponse('You must be logged in to perform this action')
        
        group_id = request.POST.get('group_id')

        if not group_id:
            return HttpResponse('Please provide group ID')

        student = StudentUser.objects.get(id=request.user.id)

        if student.username == 'admin':
            return HttpResponse('You cannot perform this action')

        if not Group.objects.filter(id=group_id).exists():
            return HttpResponse('Group doesn\'t exist')

        group = Group.objects.get(id=group_id)

        if GroupMembership.objects.filter(group=group, student=student).exists():
            return HttpResponse('You are already a member')
        
        group.members_count += 1
        group.save()
        
        group_membership = GroupMembership.objects.create(group=group, student=student)

        return HttpResponse('Group joined')

    return HttpResponse('Incorrect REST method')

def leave_group(request):
    if request.method == 'POST':

        if not request.user.is_authenticated:
            return HttpResponse('You must be logged in to perform this action')
        
        group_id = request.POST.get('group_id')

        if not group_id:
            return HttpResponse('Please provide group ID')

        student = StudentUser.objects.get(id=request.user.id)
        if student.username == 'admin':
            return HttpResponse('You cannot perform this action')

        if not Group.objects.filter(id=group_id).exists():
            return HttpResponse('Group doesn\'t exist')

        group = Group.objects.get(id=group_id)

        if not GroupMembership.objects.filter(group=group, student=student).exists():
            return HttpResponse('You must be a group member to perform this action')
        
        group_membership = GroupMembership.objects.get(group=group, student=student)
        group.admin = StudentUser.objects.get(username='admin')
        if group.members_count - 1 >= 1:
            group.members_count -= 1
        group.save()
        group_membership.delete()

        return HttpResponse('Group left')

    return HttpResponse('Incorrect REST method')

def get_my_groups(request):
    if request.method == 'GET':

        if not request.user.is_authenticated:
            return HttpResponse('You must be logged in to perform this action')
        
        student = StudentUser.objects.get(id=request.user.id)

        if not GroupMembership.objects.filter(student=student).exists():
            return HttpResponse('You have not joined any Groups')

        data = {}
        for join_info in GroupMembership.objects.filter(student=student):
            data[join_info.group.id] = (join_info.group.name, str(join_info.joined_at)[:10])
        
        return JsonResponse(data)

    return HttpResponse('Incorrect REST method')

def make_post(request):
    
    if request.method == 'POST':

        if not request.user.is_authenticated:
            return HttpResponse('You must be logged in to perform this action')
        
        student = StudentUser.objects.get(id=request.user.id)

        title = request.POST.get('title')
        content = request.POST.get('content')
        group_id = request.POST.get('group_id')

        if not title or not content or not group_id:
            return HttpResponse('Please add the requirement information')
        
        if not Group.objects.filter(id=group_id).exists():
            return HttpResponse('Group doesn\'t exist')
        
        group = Group.objects.get(id=group_id)

        if not GroupMembership.objects.filter(group=group, student=student).exists():
            return HttpResponse('You must be a member of the group to post')
        
        post = Post.objects.create(poster=student,group=group,title=title.strip(), content=content.strip())

        return HttpResponse('Post created')

    return HttpResponse('Incorrect REST method')

def get_my_posts(request):

    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponse('You must be logged in to perform this action')
        
        data = json.loads(request.body)
        student = StudentUser.objects.get(id=request.user.id)

        if 'group_id' in data:
            if not Group.objects.filter(id=data['group_id']).exists():
                return HttpResponse('Group doesn\'t exist')
            
            group = Group.objects.get(id=data['group_id'])
            posts = Post.objects.filter(group=group, poster=student)
        else:
            posts = Post.objects.filter(poster=student)
        
        data = {}
        for post in posts:
            post_data = {}
            post_data['title'] = post.title
            post_data['posted_on'] = post.posted_on
            data[post.id] = post_data
            
        return JsonResponse(data)

    return HttpResponse('Incorrect REST method')

def view_posts(request):
    
    if request.method == 'GET':

        data = json.loads(request.body)

        if not 'group_id' in data:
            return HttpResponse('Please share Group to view posts')
        
        group_id = data['group_id']

        if not Group.objects.filter(id=group_id).exists():
            return HttpResponse('Group doesn\'t exist')
        
        group = Group.objects.get(id=group_id)

        posts = Post.objects.filter(group=group)

        data = {}
        for post in posts:
            post_data = {}
            post_data['title'] = post.title
            post_data['posted_on'] = post.posted_on
            post_data['poster'] = post.poster.username
            data[post.id] = post_data
        
        return JsonResponse(data)

    return HttpResponse('Incorrect REST method')

def view_post(request, post_id):

    if request.method == 'GET':

        data = json.loads(request.body)

        if not 'group_id' in data:
            return HttpResponse('Please share Group ID')
        
        group_id = data['group_id']
        
        if not Group.objects.filter(id=group_id).exists():
            return HttpResponse('Group doesn\'t exist')
        
        group = Group.objects.get(id=group_id)

        if not Post.objects.filter(id=post_id, group=group).exists():
            return HttpResponse('Post doesn\'t exist')

        post = Post.objects.get(id=post_id, group=group)

        data = {}
        data['title'] = post.title
        data['content'] = post.content
        data['poster'] = post.poster.username
        data['posted_on'] = post.posted_on

        return JsonResponse(data)

    return HttpResponse('Incorrect REST method')

def delete_post(request, post_id):

    if request.method == 'DELETE':

        if not request.user.is_authenticated:
            return HttpResponse('You must be logged in to perform this action')

        data = json.loads(request.body)

        if not 'group_id' in data:
            return HttpResponse('Please share Group ID')
        
        group_id = data['group_id']

        if not Group.objects.filter(id=group_id).exists():
            return HttpResponse('Group doesn\'t exist')
        
        group = Group.objects.get(id=group_id)
        student = StudentUser.objects.get(id=request.user.id)
        admin = StudentUser.objects.get(id=group.admin.id)

        if not Post.objects.filter(group=group, id=post_id).exists():
            return HttpResponse('Post doesn\'t exist')
        
        post = Post.objects.get(group=group, id=post_id)

        if post.poster != student and post.poster != admin:
            return HttpResponse('You don\'t have required permission')

        post.delete()

        return HttpResponse('Post deleted')

    return HttpResponse('Incorrect REST method')

def get_pinned_post(request, group_id):

    if request.method == 'GET':
        
        if not Group.objects.filter(id=group_id).exists():
            return HttpResponse('Group doesn\'t exist')
        
        group = Group.objects.get(id=group_id)

        if not PinnedPost.objects.filter(group=group).exists():
            return HttpResponse('No pinned post for this Group')
        
        pinned_post = PinnedPost.objects.get(group=group)

        if pinned_post.post == None:
            return HttpResponse('No pinned post for this Group')
        
        post_data = {}
        post_data['post_id'] = pinned_post.post.id
        post_data['title'] = pinned_post.post.title
        post_data['poster'] = pinned_post.post.poster.username
        post_data['posted_on'] = pinned_post.post.posted_on

        return JsonResponse(post_data)

    return HttpResponse('Incorrect REST method')

def post_comment(request, post_id):

    if request.method == 'POST':

        if not request.user.is_authenticated:
            return HttpResponse('You must be logged in to perform this action')
        
        if not Post.objects.filter(id=post_id).exists():
            return HttpResponse('Post doesn\'t exist')
        
        if not request.POST.get('comment'):
            return HttpResponse('Please share the comment')
        
        post = Post.objects.get(id=post_id)
        student = StudentUser.objects.get(id=request.user.id)

        comment = Comment.objects.create(post=post, poster=student, comment=request.POST.get('comment'))

        return HttpResponse('Commet added')

    return HttpResponse('Incorrect REST method')

def delete_comment(request, post_id):

    if request.method == 'DELETE':

        if not request.user.is_authenticated:
            return HttpResponse('You must be logged in to perform this action')
        
        student = StudentUser.objects.get(id=request.user.id)
        
        data = json.loads(request.body)

        if not 'comment_id' in data:
            return HttpResponse('Please share comment ID')
        
        comment_id = data['comment_id']
        
        if not Post.objects.filter(id=post_id).exists():
            return HttpResposne('Post doesn\'t exist')
        
        if not Comment.objects.filter(id=comment_id).exists():
            return HttpResponse('Comment doesn\'t exist')
        
        comment = Comment.objects.get(id=comment_id)

        if comment.poster != student and student != comment.post.group.admin:
            return HttpResponse('You don\'t have permission to perform this action')

        comment.delete()

        return HttpResponse('Comment deleted')

    return HttpResponse('Incorrect REST method')

def view_comments(request, post_id):

    if request.method == 'GET':
        
        if not Post.objects.filter(id=post_id).exists():
            return HttpResponse('Post doesn\'t exist')
        
        post = Post.objects.get(id=post_id)

        data = {}
        for comment in Comment.objects.filter(post=post):
            comment_data = {}
            comment_data['commenter'] = comment.poster.username
            comment_data['comment'] = comment.comment
            comment_data['commented_on'] = comment.commented_on
            data[comment.id] = comment_data
        
        return JsonResponse(data)

    return HttpResponse('Incorrect REST method')

def toggle_like_post(request, post_id):

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse('You must be logged in to perform this action')
        
        student = StudentUser.objects.get(id=request.user.id)
        
        if not Post.objects.filter(id=post_id).exists():
            return HttpResponse('Post doesn\'t exist')
        
        post = Post.objects.get(id=post_id)

        if PostVotes.objects.filter(post=post, student=student).exists():
            postvote = PostVotes.objects.get(post=post, student=student)
            postvote.delete()
        else:
            postvote = PostVotes.objects.create(post=post, student=student)
        
        return HttpResponse(f"Updated likes: {PostVotes.objects.filter(post=post).count()}")
    
    return HttpResponse('Incorrect REST method')
