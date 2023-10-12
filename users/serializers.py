from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth import authenticate
from rest_framework import exceptions

from rest_framework.generics import get_object_or_404
from users.models import User
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotFound

from django.contrib.auth.hashers import check_password

<<<<<<< HEAD
=======
from wishes.serializers import WishSerializer
>>>>>>> f90159af0c3add8876df2362c9a4d009145688af

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "profile_img", "birthday",
                  "following", "created_at", "updated_at")


class UserSerializer(serializers.ModelSerializer):

    """ 회원가입 페이지, 회원 정보 수정 페이지에서 사용자가 보내는 JSON 형태의 데이터를 역직렬화하여 모델 객체 형태의 데이터를 생성하기 위한 Serializer 입니다. """
    # 이메일 중복 검증
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator]
    )

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ("username", "password", "email", "profile_img", "birthday")

    def create(self, validated_data):
        """회원가입 시 사용자가 보내는 JSON 형태의 데이터를 모델 객체의 형태로 역직렬화하는 메서드입니다."""
        user = super().create(validated_data)
        # print(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

    # def create(self, validated_data):
    #     password = validated_data.pop("password")

    #     user = User.objects.create(**validated_data)

    #     user.set_password(password)
    #     user.save()
    #     return user

    def update(self, instance, validated_data):
        """email은 수정되지 않도록, 나머지 필드는 수정되도록 설정했습니다."""
        # password hashing
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        email = instance.email  # 프론트 단에서 email 받지 못하게끔 설정 필요. 설정 시 삭제 가능한 부분.

        # 나머지 필드 업데이트
        for key, value in validated_data.items():
            setattr(instance, key, value)

        # 프론트 단에서 email 받지 못하게끔 설정 필요. 설정 시 삭제 가능한 부분.
        setattr(instance, 'email', email)

        instance.save()
        return instance


class LoginSerializer(TokenObtainPairSerializer):
    """DRF의 JWT 로그인 방식에 사용되는 TokenObtainPairSerializer를 상속하여 Serializer를 커스터마이징하여 재정의합니다."""

    def validate(self, attrs):
        user = get_object_or_404(User, email=attrs[self.username_field])

        if check_password(attrs['password'], user.password) == False:
            raise NotFound("사용자를 찾을 수 없습니다. 로그인 정보를 확인하세요.") # 404 Not Found
        elif user.is_active == False:
            raise AuthenticationFailed("이메일 인증이 필요합니다.") # 401 Unauthorized
        else:
            # 기본 동작을 실행하고 반환된 데이터를 저장합니다.
            data = super().validate(attrs)
            return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['username'] = user.username
        token['profile_img'] = user.profile_img.url

        return token

class FeedSerializer(serializers.ModelSerializer):

    following_wishes = serializers.SerializerMethodField()
    
    def get_following_wishes(seld, obj):
        followee_list = obj.following.all()
        all_wishes = []
        for followee in followee_list :
            followee_wishes = followee.wishes.all().order_by('-created_at')
            all_wishes.extend(followee_wishes)
            
        all_wishes = sorted(all_wishes, key=lambda x: x.created_at, reverse=True)
        return WishSerializer(instance=all_wishes, many=True).data

    class Meta:
        model = User
        fields = ["following_wishes"]

class MyPageSerializer(serializers.ModelSerializer):
    follower = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    like_wishes = serializers.SerializerMethodField()
    bookmark_wishes = serializers.SerializerMethodField()
    wishes = serializers.SerializerMethodField()

    def get_follower(self, obj):
        follower_list = obj.followers.all().order_by('-id')
        return UserSerializer(instance=follower_list, many=True).data
    
    def get_following(self, obj):
        followee_list = obj.following.all().order_by('-id')
        return UserSerializer(instance=followee_list, many=True).data

    def get_follower_count(self, obj):
        return obj.followers.count()
    
    def get_following_count(self, obj):
        return obj.following.count()
    
    def get_like_wishes(self, obj):
        like_wishes = obj.likes.all().order_by('-created_at')
        return WishSerializer(instance=like_wishes, many=True).data
    
    def get_bookmark_wishes(self, obj):
        bookmark_wishes = obj.bookmarks.all().order_by('-created_at')
        return WishSerializer(instance=bookmark_wishes, many=True).data

    def get_wishes(self, obj):
        wishes=obj.wishes.all().order_by('-created_at')
        return WishSerializer(instance=wishes, many=True).data

    class Meta:
        model = User
        fields = ["follower", "following", "follower_count", "following_count", "like_wishes", "bookmark_wishes", "profile_img", "wishes"]