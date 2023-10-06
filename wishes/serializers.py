from rest_framework import serializers
from wishes.models import Comment, Wish


class WishCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = ("title", "wish_name", "content", "wish_img")


class WishSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.email

    class Meta:
        model = Wish
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)
