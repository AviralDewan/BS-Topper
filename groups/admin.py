from django.contrib import admin
from .models import Group, GroupMembership, Post, PinnedPost, Comment, PostVotes

admin.site.register(Group)
admin.site.register(GroupMembership)
admin.site.register(Post)
admin.site.register(PinnedPost)
admin.site.register(Comment)
admin.site.register(PostVotes)
