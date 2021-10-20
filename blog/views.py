from django.http import Http404

from rest_framework import generics, status, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings

from core.models import Tag, Post
from .serializers import TagDetailSerializer, TagSerializer, PostSerializer
from .paginators import PostPagination


def _get_tag_object(tag_slug):
    """ Return Tag based in its slug """
    try:
        return Tag.objects.get(slug=tag_slug)
    except Tag.DoesNotExist:
        raise Http404


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
    """ Retrieve all instance tags """

    def get(self, request, format=None):
        """ Return a list of all tags """
        tags = Tag.objects.all().order_by('name')
        serializer = TagDetailSerializer(tags, many=True)
        return Response(serializer.data)


class TagDetail(APIView):
    """ Retrieve a tag instance """

    def get(self, request, tag_slug, format=None):
        """ Returns Tag """
        tag = _get_tag_object(tag_slug=tag_slug)
        serializer = TagDetailSerializer(tag)
        return Response(serializer.data)


class TagView(APIView):
    """ Create or update a tag instance with authenticated user """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        """ Creates a Tag object """
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, tag_slug):
        """ Update Tag with authenticated user """
        tag = _get_tag_object(tag_slug=tag_slug)
        serializer = TagSerializer(tag, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=statys.HTTP_400_BAD_REQUEST)
