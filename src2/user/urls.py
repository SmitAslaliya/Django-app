from django.urls import path
from .views import UserCreateView, UserLoginView, UserLogoutView,UserChangePasswordView,UnfollowUser,UserFollowerView,PostLikeView , CommentView,UserProfileView

urlpatterns = [
    path('create-user', UserCreateView.as_view()),
    path('login', UserLoginView.as_view()),
    path('logout', UserLogoutView.as_view()),
    path('change-password', UserChangePasswordView.as_view()),
    # path('follow',Userfollowing.as_view()),
    # path('all-user',AllUser.as_view()),
    path('unfollow',UnfollowUser.as_view()),
    path('follow', UserFollowerView.as_view()),
    path('like/', PostLikeView.as_view()),
    path('comment/', CommentView.as_view()),
    path('profile', UserProfileView.as_view()),
]
