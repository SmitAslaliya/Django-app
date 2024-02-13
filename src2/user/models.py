from django.db import models
from django.contrib.auth.models import User
from post.models import Post

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_follow')
    following= models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} | {self.following.username}"
    
class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_like')    #login user
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')     #post of user
    created_at = models.DateTimeField(auto_now_add=True)
    
class Comment(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE, related_name="user_comment")
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="Comments")
    comment = models.CharField(max_length = 256)
    created_at = models.DateTimeField(auto_now_add=True)
