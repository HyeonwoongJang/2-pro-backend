from rest_framework import serializers
from wishes.models import Comment, Wish, WishImage, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tags']


class WishImageSerializer(serializers.ModelSerializer):
    # use_url=True : 이미지 URL을 사용하도록 설정, 이미지의 URL을 JSON 응답에 포함시킴.
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = WishImage
        fields = ['image']


class WishCreateSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    tags = serializers.ListField(
        child=serializers.CharField(), write_only=True)  # 태그 이름을 문자열로 받기 위해 추가

    # 게시글에 등록된 이미지들 가지고 오기

    def get_images(self, obj):
        image = obj.image.all()
        return WishImageSerializer(instance=image, many=True, context=self.context).data

    class Meta:
        model = Wish
        # fields = "__all__"
        exclude = ("likes", "bookmarks")

    def create(self, validated_data):
        instance = Wish.objects.create(**validated_data)
        instance.tags.set(tags)
        tag_names = validated_data.pop('tag_names')
        if tag_names:
            tags = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                tags.append(tag)

        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            WishImage.objects.create(wish=instance, image=image_data)
        return instance

    def update(self, instance, validated_data):
        tag_names = validated_data.pop('tag_names')
        if tag_names:
            tags = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                tags.append(tag)

        instance.tags.set(tags)
        instance.image.all().delete()
        image_set = self.context['request'].FILES.getlist('image')
        for image_data in image_set:
            WishImage.objects.create(wish=instance, image=image_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class WishListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    bookmarks_count = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    # 게시글에 등록된 이미지들 가지고 오기
    def get_images(self, obj):
        image = obj.image.all()
        return WishImageSerializer(instance=image, many=True, context=self.context).data

    def get_author(self, obj):
        return obj.author.username

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_bookmarks_count(self, obj):
        return obj.bookmarks.count()

    class Meta:
        model = Wish
        fields = ("id", "author", "title", "wish_name", "content", "tags"
                  "images", "likes_count", "bookmarks_count", "created_at")


# comment 정보를 불러오기 위해선 author, content, created_at 모두 있어야 함.
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("author", "content", "created_at")


class WishSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likes = serializers.StringRelatedField(many=True)
    bookmarks = serializers.StringRelatedField(many=True)
    images = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True)  # 특정 wish에 작성된 comment list 불러오기
    # 특정 wish에 작성된 comments 개수 세기
    comments_set_count = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)

    def get_comments_set_count(self, obj):
        return obj.comments.count()

    # 게시글에 등록된 이미지들 가지고 오기

    def get_images(self, obj):
        image = obj.image.all()
        return WishImageSerializer(instance=image, many=True, context=self.context).data

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
