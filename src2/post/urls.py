from django.urls import path
from .views import delete_post, get_post, create_post, update_post, post_operations,PostImageView,PostOperationView,CreatePostView,SearchView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', get_post),
    path('create', create_post),
    path('update', update_post),
    path('delete', delete_post),
    path('operations', post_operations),
    path('class-based-path', PostOperationView.as_view()),
    path('post-image',PostImageView.as_view()),
    path('create-post-img',CreatePostView.as_view()),
    path('search', SearchView.as_view())
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
