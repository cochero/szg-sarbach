from django.shortcuts import render, get_object_or_404
from .models import BlogPost


def blog_list(request, post_type='Blog'):
    posts = BlogPost.objects.filter(post_type=post_type, is_active=True)
    type_labels = {'Blog': 'Blogs', 'Event': 'Events', 'WorkShop': 'Workshops'}
    return render(request, 'blog_app/blog_list.html', {
        'posts': posts,
        'post_type': post_type,
        'page_title': type_labels.get(post_type, 'Posts'),
    })


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_active=True)
    related = BlogPost.objects.filter(post_type=post.post_type, is_active=True).exclude(id=post.id)[:3]
    return render(request, 'blog_app/blog_detail.html', {
        'post': post,
        'related_posts': related,
    })
