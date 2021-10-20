from rest_framework import serializers

from core.models import Tag, Post


class TagDetailSerializer(serializers.ModelSerializer):
    """ Serializer for Tag model """
    # posts = serializers.PrimaryKeyRelatedField(
    #     queryset=Post.objects.all(), many=True)
    posts = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug'
    )

    class Meta:
        model = Tag
        fields = (
            'name',
            'slug',
            'get_absolute_url',
            'posts'
        )


class TagSerializer(serializers.ModelSerializer):
    """ Serializer for Tag model """
    class Meta:
        model = Tag
        fields = ('name',)

    def validate_name(self, value):
        if value:
            return value
        raise serializers.ValidationErrors('Name must be present.')


class PostSerializer(serializers.ModelSerializer):
    """ Serializer for Post model """
    tags = TagDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            'title',
            'get_absolute_url',
            'body',
            'description',
            'publish',
            'updated_at',
            'tags'
        )
