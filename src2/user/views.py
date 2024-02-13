from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from post.models import PostPermission,Post
from .models import Follow,PostLike,Comment
from .serializers import FollowerSerializer,FollowingSerializer
from post.serialization import UserProfileSerializer

from rest_framework.permissions import IsAuthenticated

# Create your views here.

class UserCreateView(APIView):
    def post(self, request):
        data = request.data
        try:
            username = data['username']
            email = data['email']
            password = data['password']
        except Exception as key:
            return Response({str(key) : ['field required']})
        
        if User.objects.filter(username=username).exists():
            return Response({'username':["this user already exists"]},status=400)
        
        user = User.objects.create(email=email, username=username)
        user.set_password(password)
        user.save()
        PostPermission.objects.create(user=user)



        with get_connection(host=settings.EMAIL_HOST, 
                            port=settings.EMAIL_PORT,  
                            username=settings.EMAIL_HOST_USER,  
                            password=settings.EMAIL_HOST_PASSWORD,  
                            use_tls=settings.EMAIL_USE_TLS) as connection:  
            recipient_list = ['smitaslaliya@gmail.com']  
            subject = 'Test Email' 
            email_from = settings.EMAIL_HOST_USER  
            message = "Hello How are? Khana kha ke jana ha!" 
            EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()
        
        res = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            }

        
        return Response({"message": "User created", "user": res})
    
class UserLoginView(APIView):
    def post(self, request):
        data = request.data
        request.data["username"]
        user_name = request.data.get("username")
        password = data['password']

        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return Response({"error":"User not found"}, status=404)
        
        if authenticate(username=user_name, password=password):
            # token, created = Token.objects.get_or_create(user=user)

            token, created = Token.objects.update_or_create(user=user)
            if not created:
                token.delete()
                token = Token.objects.create(user=user)

            
            # print("token -- " , token)
            # print("created -- ", created)

            response = {
                'username': user.username,
                'email': user.email,
                'usertype': 'admin',
                'token': str(token)
                }
            return Response(response, status=200)
        return Response({"message": "Invalid Credientials"}, status=status.HTTP_401_UNAUTHORIZED)



class UserLogoutView(APIView):
    authentication_classes = (TokenAuthentication, )
    def delete(self, request):
        try:
            Token.objects.get(user=request.user).delete()
            return Response({"message":"user logout"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"message": "user already logout"}, status=status.HTTP_404_NOT_FOUND)
        



class UserChangePasswordView(APIView):
    authentication_classes = (TokenAuthentication,)
    
    def post(self, request):
        data = request.data

        current_password = data['current_password']
        password1 = data['password1']
        password2 = data['password2']


        if authenticate(username=request.user.username, password=current_password):
            if password1 == password2:
                request.user.set_password(password1)
                request.user.save()
                return Response({'message':'successfully changed password'}, status=status.HTTP_200_OK)
            else:
                return Response({"message" : 'new password are not same'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "invalid password"}, status=status.HTTP_400_BAD_REQUEST)

# class Follow(APIView):
#     authentication_classes = (TokenAuthentication,)
# # date-31-1 post,get completed
#     def post(self, request):
#         x = int(request.query_params.get('id'))
#         y = request.user.id                    #for getting user id from token
#         if y == x:                             
#             return Response('user can not follow themselves')
              
#         exist_folloiwng = Follow.objects.filter(follow_to=x,follow_by=y).exists()   
#         #for not follow multiple times
#         if exist_folloiwng:
#             return Response('already followed')
    
#         follower_user = User.objects.get(id = request.query_params.get('id'))
        
#         print(follower_user)
#         following = Follow.objects.create(follow_by=request.user,follow_to=follower_user)
#         following.save()
#         return Response('follow')

# class AllUser(APIView):
#     authentication_classes = (TokenAuthentication,)

#     def get(self, request):
#         try:
#             user_id = request.query_params.get('id')
#             all_following = Follow.objects.filter(follow_by=user_id).all()
#             # get_user = Follow.objects.get(pk=user_id)
#             serializer = GetAllUserSerializer(all_following,many=True)
            
#         except Follow.DoesNotExist:
#             return Response('can not fatch data')
#         return Response(serializer.data)
        

class UnfollowUser(APIView):
    authentication_classes = (TokenAuthentication,)

    def delete(self, request):
        user = request.user
        unfollow_id = request.query_params.get('id')
        user = Follow.objects.get(following=unfollow_id, user=user)
        user.delete()
                
        return Response('you unfollow a user')
    
class UserFollowerView(APIView):
    authentication_classes = (TokenAuthentication,)
    
    def get(self, request):
        user = request.user
        following = Follow.objects.filter(user=user)
        
        following_serializer = FollowingSerializer(following, many=True)
        
        follower = Follow.objects.filter(following=user)
        followers_serializer = FollowerSerializer(follower, many=True)
        
        follower_count = follower.count()
        
        following_count = following.count()
        
        res = {
            "user_id": user.id,
            "user_name":user.username,
            "following":following_serializer.data,
            "follower":followers_serializer.data,
            "following_count":following_count,
            "follower_count":follower_count,
        }
        
        return Response(res)
    
class PostLikeView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        post_id = request.data.get("post_id")
        
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the user already liked the post
        if PostLike.objects.filter(user=user, post_id=post_id).exists():
            return Response({"message": "User already liked this post"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new PostLike instance
        post_like = PostLike(user=user, post_id=post)
        post_like.save()
        
        # Update the post_likes count in the Post model
        post.post_likes = PostLike.objects.filter(post_id=post).count()
        post.save()
        
        # Return the updated count of likes
        return Response({"like_count": post.post_likes}, status=status.HTTP_200_OK)
    
class CommentView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        post_id = request.data.get("post_id")
        comment = request.data.get('comment')
        
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        post_comment = Comment(user=user, post_id=post , comment = comment )
        post_comment.save()
        
        # # Update the post_likes count in the Post model
        post.post_comment = Comment.objects.filter(post_id=post_id).count()
        post.save()
        
        
        # Return the updated count of likes
        return Response({"comment_count": post.post_comment}, status=status.HTTP_200_OK)
        
class UserProfileView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
        