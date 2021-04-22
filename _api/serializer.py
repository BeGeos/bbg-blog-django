from rest_framework import serializers
from post.models import Post, PostTag
from news.models import News, NewsTag


class PostSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = ["title", "summary", "post", "likes", "views",
                  "created_on", "author", "slug", "tags",
                  "image"]


class NewsSerializer(serializers.ModelSerializer):
    pass
