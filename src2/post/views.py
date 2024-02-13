from django.shortcuts import render

# Create your views here.
from datetime import datetime
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.shortcuts import render
from post.UserPostPermissions import PostDeletePermission

from .serialization import PostSearializer,PostImageSerializer,UserProfileSerializer
from .models import Post
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
# from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q

@api_view(['GET'])
def get_post(request):

    # posts = Post.objects.all()

    # try:
    #     post = Post.objects.get(title = 'Third Post')
    #     print(post)
    # except Post.DoesNotExist:
    #     print('Post Not Found')
    # except Post.MultipleObjectsReturned:
    #     print("Some thing went wrong")

    posts = Post.objects.filter(pk=3)

    data = []

    for post in posts:
        context = {
        'id' : post.id,
        'title' : post.title,
        'content' : post.content,
        'date_posted' : post.date_posted,
        'author' : post.author.username,
        'date_updated' : post.date_updated
        }

        data.append(context)

    return HttpResponse(data)


@api_view(['POST'])
def create_post(request):
    data = request.data
    post_title = data.get('title')
    post_contain = data.get('contain')

    if request.user.is_authenticated:
        post_user = request.user
    else:
        return Response({"message" : "login required"}, status=status.HTTP_401_UNAUTHORIZED)

    # post_user = request.user if request.user != 'AnonymousUser' else None

    print(post_user)
    print("=============")

    post = Post.objects.create(title=post_title, content=post_contain, author=post_user)
    post_count = Post.objects.count()

    serializer = UserProfileSerializer(post)
    return HttpResponse(post_count,serializer.data)


@api_view(['PATCH'])
def update_post(request):
    data = request.data

    post_id = data.get('id')
    post_title = data.get('title')
    post_contain = data.get('contain')
    if not post_id:
        return Response({"message": "Post id requred"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return HttpResponse('Post not found')
    
    try:
        user = User.objects.get(username='admin')
    except User.DoesNotExist:
        return HttpResponse("User not found")
    
    if user:
        post.author = user

    if post_title:
        post.title = post_title

    if post_contain:
        post.content = post_contain

    post.date_updated = timezone.now()

    post.save()

    return HttpResponse(f"post updated {post}")

def delete_post(request):
    try:
        post = Post.objects.get(pk=5)
    except Post.DoesNotExist:
        return HttpResponse('Post not found')
    
    post.delete()

    return HttpResponse('Post deleted')


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def post_operations(request):
    if request.method == 'GET':
        post_id = request.query_params.get('id')
        search_by = request.query_params.get('search')


        if post_id:
            try:
                post = Post.objects.get(pk=post_id)
            except Post.DoesNotExist:
                return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = PostSearializer(post)

            return Response(serializer.data, status=status.HTTP_200_OK)
            
        elif search_by:
            posts = Post.objects.filter(title__contains=search_by)

            serializer = PostSearializer(posts, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
    elif request.method == 'POST':

        data = request.data

        post_user = User.objects.get(username='admin')

        serializer = PostSearializer(data=data)
        if serializer.is_valid():
            serializer.save(author=post_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        data = request.data

        post_id = request.query_params.get('id')

        if not post_id:
            return Response({"message": "Post id requred"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return HttpResponse('Post not found')
        
        serializer = PostSearializer(post, data=data, partial=True)
        if serializer.is_valid():
            serializer.save(date_updated = timezone.now())
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        post_id = request.query_params.get('id')

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return HttpResponse('Post not found')
        
        post.delete()

        return Response({"message": "Post deleted"}, status=status.HTTP_204_NO_CONTENT)
    



class PostOperationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [PostDeletePermission, IsAuthenticated]

    def get(self, request):
        post_id = request.query_params.get('id')
        search_by = request.query_params.get('search')

        if post_id:
            try:
                post = Post.objects.get(pk=post_id)
            except Post.DoesNotExist:
                return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = PostSearializer(post)

            return Response(serializer.data, status=status.HTTP_200_OK)
            
        elif search_by:
            posts = Post.objects.filter(title__contains=search_by)

            serializer = PostSearializer(posts, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Something went worng"}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        data = request.data
        x= request.user.id
        print(x)
        data['author'] = x

        # post_user = User.objects.get(username='admin')

        serializer = PostSearializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        id = request.query_params.get("id")

        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return Response({"error":"Post does not exist."}, status=status.HTTP_404_NOT_FOUND)
        # Checking user permission to perform this action

        post.delete()

        return Response({"message": "Post deleted"}, status=status.HTTP_200_OK)

class PostImageView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]    
    def post(self, request, *args, **kwargs):
        post_id= request.data.get('post')
        try:
            post = Post.objects.get(id = post_id)
        except Post.DoesNotExist:
            return Response('post not found')
        imgSerializer = PostImageSerializer(data=request.data)
        if imgSerializer.is_valid():
            imgSerializer.save()
            return Response(imgSerializer.data, status=status.HTTP_200_OK)
        return Response(imgSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreatePostView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data
        
        post_serializer = PostImageSerializer(data=data)
        if post_serializer.is_valid():
            post_serializer.save()
            
            image_data = {
                "image": request.data.get('image'),
                "post":request.data.get('id'),
            }
            img_serializer = PostImageSerializer(data=image_data)    
            if img_serializer.is_valid():
                img_serializer.save()
            else:
                return Response(img_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            response = {}
            response.update(post_serializer.data)
            response.update(img_serializer.data)
            return Response(response, status=status.HTTP_201_CREATED)
        
        else:
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class SearchView(APIView):
    def get(self, request):
        users = User.objects.all()
        search_query = "harshit"
        
        q= Q
        
        if search_query:
            users = users.filter(Q(username__contains=search_query) | Q(username__contains="admin"))
            print(users)
        return Response({})