from rest_framework import serializers
from .models import Follow,PostLike
from post.models import User


class FollowingSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    class Meta:
        model=Follow
        fields = ["user_id","user_name"]
        
    def get_user_id(self, obj):
        return obj.following.id
    
    def get_user_name(self, obj):
        return obj.following.username
        
class FollowerSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
        
    class Meta:
        model = Follow
        fields = ["user_id","user_name"]
        
    def get_user_id(self, obj):
        return obj.user.id
    
    def get_user_name(self, obj):
        return obj.user.username
                
        
class GetAllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id','follow_by']

class PostLikeSerializer(serializers.ModelSerializer):
    post_id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    
    class Meta:
        model = PostLike
        fields = ["post_id","user_id"]
        

