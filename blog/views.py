from django.http import Http404

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import Tag, Post
from .serializers import TagSerializer, PostSerializer
from .paginators import PostPagination


class AllPosts(generics.ListAPIView):
    """ Return a list of all posts """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination


class PostDetail(APIView):
    """ Return a single Post """

    def _get_object(self, post_slug):
        """ Return a post based on its slug """
        try:
            return Post.objects.get(slug=post_slug)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, post_slug, format=None):
        """ Returns post """
        post = self._get_object(post_slug)
        serializer = PostSerializer(post)
        return Response(serializer.data)


class AllTags(APIView):
    def get(self, request, format=None):
        """ Return a list of all tags """
        tags = Tag.objects.all().order_by('name')
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)


class TagDetail(APIView):
    def _get_object(self, tag_slug):
        """ Return Tag based on its slug """
        try:
            return Tag.objects.get(slug=tag_slug)
        except Tag.DoesNotExist:
            raise Http404

    def get(self, request, tag_slug, format=None):
        """ Returns Tag """
        tag = self._get_object(tag_slug)
        serializer = TagSerializer(tag)
        return Response(serializer.data)
