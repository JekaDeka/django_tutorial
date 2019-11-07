from django.contrib.auth.decorators import login_required
from django.shortcuts import (get_object_or_404, redirect, render,
                              render_to_response)
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.views import ActionSerializedViewSet

from .forms import CommentForm, PostForm
from .models import Comment, Post
from .serializers import (BlogPostCreateUpdateSerializer,
                          BlogPostDetailSerializer, BlogPostListSerializer,
                          CommentSerializer)


def post_list(request):
    posts = Post.objects.for_user(user=request.user)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_edit(request, id=None):
    post = get_object_or_404(Post, id=id) if id else None

    if post and post.author != request.user:
        return redirect('post_list')

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if post.is_published:
                post.published_date = timezone.now()
            else:
                post.published_date = None
            post.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_publish(request, id):
    post = get_object_or_404(Post, id=id)
    post.publish()
    return redirect('post_detail', id=id)


def add_comment(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', id=post.id)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form})


def handler404(request, exception, template_name="404.html"):
    response = render_to_response("404.html")
    response.status_code = 404
    return response


class CommentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing comments instances.
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class BlogPostViewSet(ActionSerializedViewSet):
    """
    A viewset for viewing and editing blog posts instances.
    """
    serializer_class = BlogPostListSerializer
    queryset = Post.objects.all()

    action_serializers = {
        'list': BlogPostListSerializer,
        'retrieve': BlogPostDetailSerializer,
        'create': BlogPostCreateUpdateSerializer,
        'update': BlogPostCreateUpdateSerializer,
    }

    def get_queryset(self):
        queryset = self.queryset
        author = self.request.query_params.get('author', None)
        if author:
            queryset = queryset.filter(author__username=author)
        return queryset

    @action(detail=False)
    def published_posts(self, request):
        published_posts = Post.published.all()

        page = self.paginate_queryset(published_posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(published_posts, many=True)
        return Response(serializer.data)

    @action(detail=True,
            methods=['post'],
            permission_classes=[IsAuthenticated])
    def publish(self, request, pk=None):
        post = self.get_object()
        if request.user == post.author:
            post.publish()
            return Response({'message': 'blog post was published'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You don\t have permissions'},
                            status=status.HTTP_403_FORBIDDEN)
