from rest_framework import serializers
from .models import Comment, Post
from django.contrib.contenttypes.models import ContentType


class CommentSerializer(serializers.ModelSerializer):
    comment_rating = serializers.SerializerMethodField()
    thread_rating = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'timestamp', 'content',
                  'parent', 'comment_rating', 'thread_rating']

    def get_comment_rating(self, obj):
        return obj.total_rating()

    def get_thread_rating(self, obj):
        return obj.calculate_thread_rating()


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'parent', 'content_type', 'object_id']


class PostSerializer(serializers.ModelSerializer):
    content_type_id = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'content_type_id']

    def get_content_type_id(self, obj):
        content_type = ContentType.objects.get_for_model(Post)
        return content_type.id


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content']
