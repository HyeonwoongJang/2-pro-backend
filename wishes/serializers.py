from rest_framework import serializers
from wishes.models import Wish

class WishCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = ("title", "wish_name", "content", "wish_img")

class WishSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        """
        Wish 모델의 author 필드는 ForeignKey입니다.
        author필드를 정참조하여 참조 모델 객체(User)의 username 필드 값을 반환합니다.
        """
        return obj.author.username

    likes = serializers.StringRelatedField(many=True)
    bookmarks = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Wish
        fields = "__all__"