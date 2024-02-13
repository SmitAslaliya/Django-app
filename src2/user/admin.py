from django.contrib import admin
from .models import Follow , Comment , PostLike
# Register your models here.

class FollowAdmin(admin.ModelAdmin):
    model = Follow
    
    list_display = ['id','user','following']
    
admin.site.register(Follow,FollowAdmin)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post_id' , 'comment']

@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['user' , 'post_id']