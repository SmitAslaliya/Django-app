from django.contrib import admin
from .models import Post, PostPermission,PostImage

# Register your models here.

# 1st Approch
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post

    list_display = ['id','author','title', 'status','date_posted',  'date_updated','post_likes' , 'post_comment' , ]

    list_filter = ['author', 'status']

    search_fields = ['author__username', 'title', 'status']

    list_editable = ['status']

    list_per_page = 10



# 2nd Approch
class PostPermissionAdmin(admin.ModelAdmin):
    model = PostPermission

    list_display = ['id', 'user', 'can_delete_post', 'can_edit_post']

    list_editable = ['can_delete_post', 'can_edit_post']

admin.site.register(PostPermission, PostPermissionAdmin)



class PostImageAdmin(admin.ModelAdmin):
    model = PostImage
    
    list_display = ['id','image']
    
admin.site.register(PostImage,PostImageAdmin)