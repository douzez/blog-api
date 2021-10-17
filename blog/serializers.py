from rest_framework import serializers

from core.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """ Serializer for Tag model """
    class Meta:
        model = Tag
        fields = (
            'name',
            'slug'
        )
