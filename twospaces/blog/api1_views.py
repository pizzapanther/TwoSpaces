from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from twospaces.blog.models import BlogPost, Category
from twospaces.blog.serializers import PostSizzler
from twospaces.utils import paginate_queryset


@api_view(['GET'])
@permission_classes((AllowAny,))
def post_detail(request, slug):
  post = get_object_or_404(BlogPost.published, slug=slug)
  sizzle = PostSizzler(post)

  return Response(sizzle.data, status=200)


@api_view(['GET'])
@permission_classes((AllowAny,))
def latest(request):
  try:
    latest_post = BlogPost.published.latest()

  except BlogPost.DoesNotExist:
    return Response(None, status=200)

  sizzle = PostSizzler(latest_post, exclude=('body',))
  return Response(sizzle.data, status=200)


@api_view(['GET'])
@permission_classes((AllowAny,))
def posts(request):
  qs = BlogPost.published.all()
  title = 'Blog'

  cat = request.GET.get('cat', '')
  if cat:
    cat = get_object_or_404(Category, slug=cat)
    qs = qs.filter(categories=cat)
    title += " \u00BB " + cat.title

  blog_posts, page, next_page, prev_page = paginate_queryset(request, qs)
  sizzle = PostSizzler(blog_posts, many=True, exclude=('body',))
  data = {
      'posts': sizzle.data,
      'page': page,
      'next': next_page,
      'prev': prev_page,
      'title': title,
  }
  return Response(data, status=200)
