from django.urls import include, path
from rest_framework import routers

# from . import views
from .views import BlogPostViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'comments', CommentViewSet)
router.register(r'posts', BlogPostViewSet)

urlpatterns = [
    # path('posts/', views.post_list, name='post_list'),
    # path('posts/<int:id>/', views.post_detail, name='post_detail'),
    # path('posts/<int:id>/edit/', views.post_edit, name='post_edit'),
    # path('posts/<int:id>/publish/', views.post_publish, name='post_publish'),
    # path('posts/<int:id>/comment/', views.add_comment, name='add_comment'),
    # path('posts/add/', views.post_edit, name='post_add'),
    path('', include(router.urls)),
]
