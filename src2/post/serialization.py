from rest_framework import serializers
from .models import Post,PostImage

class PostSearializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'
from .models import Post

class UserProfileSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # Serializes author as a string representation (e.g., username)
    post_likes = serializers.IntegerField()  # Use source to customize field name if necessary

    class Meta:
        model = Post
        fields = ["title", "content", "author", "image", "post_likes", "post_comment"]

