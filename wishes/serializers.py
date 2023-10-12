from rest_framework import serializers
from wishes.models import Comment, Wish, WishImage, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class WishImageSerializer(serializers.ModelSerializer):
    # use_url=True : 이미지 URL을 사용하도록 설정, 이미지의 URL을 JSON 응답에 포함시킴.
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = WishImage
        fields = ['image']


class WishCreateSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    tags = serializers.CharField(required=False)

    # 게시글에 등록된 이미지들 가지고 오기

    def get_images(self, obj):
        image = obj.image.all()
        return WishImageSerializer(instance=image, many=True, context=self.context).data

    class Meta:
        model = Wish
        # fields = "__all__"
        exclude = ("likes", "bookmarks")

    def create(self, validated_data):
        tags = validated_data.pop('tags')  # 필드 값을 가져오고
        tag_list = []  # 태그 모델 인스턴스 저장
        for tag in tags.split(' '):  # 스페이스로 분리해서 각 태그 이름 가져오기
            tag_instance, created = Tag.objects.get_or_create(name=tag)
            # 태그 이름으로 tag 모델 가져와서 존재하는 겨우 가져오고 없으면 생성
            tag_list += [tag_instance]
            # 찾거나 생성한 태그 인스턴스를 추가

        instance = Wish.objects.create(**validated_data)
        instance.tags.set(tag_list)

        image_set = self.context['request'].FILES

        for image_data in image_set.getlist('image'):
            WishImage.objects.create(wish=instance, image=image_data)
        return instance

    def update(self, instance, validated_data):

        tags_set = self.context['request'].data.get('tags', '')  # 필드값 가져오고
        tag_list = []  # 태그 모델 인스턴스를 저장

        for tag_name in tags_set.split(' '):  # 문자열을 분리해서 각 태그이름 가져오기
            if tag_name:  # 가져온 태그 이름이 비어있지 않을떄
                tag_instance, created = Tag.objects.get_or_create(
                    name=tag_name)
                # 각 태그 이름 사용해서 Tag 모델에서 있으면 찾거나 없으면 생성
                tag_list.append(tag_instance)
                # 추가

        instance.tags.set(tag_list, clear=True)
        # 기존 태그 모두 삭제하고 새로운 태그를 설정 하고 태그 목록으로 업뎃

        image_set = self.context['request'].FILES.getlist('image')

        instance.image.all().delete()
        for image_data in image_set:
            WishImage.objects.create(wish=instance, image=image_data)

        # for attr, value in validated_data.items():
        #     print(attr)
        #     if attr != 'tags':  # tags 필드는 이미 업데이트됨
        #         setattr(instance, attr, value)
        for attr, value in validated_data.items():
            if attr == 'tags':
                continue
            setattr(instance, attr, value)

        instance.save()
        return instance


class WishListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    bookmarks_count = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)

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
        fields = '__all__'



class CommentSerializer(serializers.ModelSerializer):   # comment 정보를 불러오기 위해선 author, content, created_at 모두 있어야 함.
    author = serializers.SerializerMethodField()
    
    def get_author(self, obj):
        return obj.author.username
    
    class Meta:
        model = Comment
        fields = ("id", "author", "content", "created_at")


class WishSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    author_id = serializers.SerializerMethodField()
    likes = serializers.StringRelatedField(many=True)       # 중복
    bookmarks = serializers.StringRelatedField(many=True)   # 중복
    likes_count = serializers.SerializerMethodField()
    bookmarks_count = serializers.SerializerMethodField()
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
    
    def get_author_id(self, obj):
        return obj.author.id

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_bookmarks_count(self, obj):
        return obj.bookmarks.count()

    class Meta:
        model = Wish
        fields = ("author", "author_id", "likes", "bookmarks", "likes_count", "bookmarks_count", "images", "comments", "comments_set_count", "title", "content", "id", "created_at", "updated_at", "wish_name")

