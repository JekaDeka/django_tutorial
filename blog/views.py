from django.http import Http404
from django.shortcuts import get_object_or_404, render, render_to_response

from .models import Post


def post_list(request):
    posts = Post.objects.for_user(user=request.user)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    if not post.is_publish() and not request.user.is_staff:
        raise Http404("Запись в блоге не найдена")
    return render(request, 'blog/post_detail.html', {'post': post})


def handler404(request, exception, template_name="404.html"):
    response = render_to_response("404.html")
    response.status_code = 404
    return response
