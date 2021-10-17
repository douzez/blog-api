from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import Tag
from .serializers import TagSerializer


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
        """ Returns tag for tag slug """
        tag = self._get_object(tag_slug)
        serializer = TagSerializer(tag)
        return Response(serializer.data)
