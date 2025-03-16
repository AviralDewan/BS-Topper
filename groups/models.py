from django.db import models
from student_auth.models import StudentUser

class Group(models.Model):
    def get_default_admin():
        return StudentUser.objects.get(username='admin')

    name = models.CharField(max_length=50)
    desc = models.TextField()
    rules = models.TextField()
    profile_pic = models.URLField()
    admin = models.ForeignKey(StudentUser, on_delete=models.SET(get_default_admin), related_name='group')
    members_count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.id}: {self.name} mod by {self.admin.username}"

class GroupMembership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='memberships')
    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE, related_name='members')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'group')
    
    def __str__(self):
        return f"{self.student.username} -> {self.group.name}"

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    poster = models.ForeignKey(StudentUser, on_delete=models.SET_NULL, related_name='posts', null=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return f"{self.id}: {self.title} by {self.poster.username} in {self.group.name}"

class PinnedPost(models.Model):
    post = models.OneToOneField(Post, on_delete=models.SET_NULL, related_name='pinned_post', null=True)
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='group')

    def __str__(self):
        return f"{self.id}: {self.group.name}"

class Comment(models.Model):
    comment = models.TextField()
    poster = models.ForeignKey(StudentUser, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commented_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: {self.poster.username} commented on post #{self.post.id}"

class PostVotes(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes')
    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE, related_name='votes')

    def __str__(self):
        return f"{self.id}: student #{self.student.username} upvoted post#{self.post.id}"
