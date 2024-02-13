from django.db import models
from django.contrib.auth.models import User
# Create your models here.
POST_STATUS_CHOICES = ( 
    ("draft", "draft"), 
    ("published", "published"),
    ("private", "private"), 
) 

def upload_images(instance, filename):  
    return f"upload/{instance.author.username}/{instance.id}/{filename}"


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to=upload_images, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='published', choices=POST_STATUS_CHOICES)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True)  
    date_updated = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    post_likes = models.IntegerField(default=0)
    post_comment = models.IntegerField(null=True,blank=True)
    
    def __str__(self) -> str:
        return str(self.author) +' | '+str(self.title)
    
    def update_likes_count(self):
        self.post_likes = self.postlike_set.count()  # Assuming the related name is 'postlike_set'
        self.save()

class PostPermission(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    can_delete_post = models.BooleanField(default=True)
    can_edit_post = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return str(self.user.username)
    
class PostImage(models.Model):
    post = models.ForeignKey(Post,on_delete = models.CASCADE, null=True)
    image = models.ImageField(upload_to=upload_images,null=True,blank=True)

    