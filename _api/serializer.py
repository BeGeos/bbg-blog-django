from rest_framework import serializers
from post.models import Post, PostImage, PostTag
from news.models import News, NewsImage, NewsTag


class PostSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(queryset=PostImage.objects.filter(is_cover=True).first(),
                                            read_only=True)
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = ["title", "summary", "post", "likes", "views",
                  "created_on", "author", "slug", "images", "tags"]


class NewsSerializer(serializers.ModelSerializer):
    pass
