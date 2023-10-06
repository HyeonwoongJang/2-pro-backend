from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "profile_img", "birthday", "following", "created_at", "updated_at")


class UserSerializer(serializers.ModelSerializer):

    """ 회원가입 페이지, 회원 정보 수정 페이지에서 사용자가 보내는 JSON 형태의 데이터를 역직렬화하여 모델 객체 형태의 데이터를 생성하기 위한 Serializer 입니다. """

    class Meta:
        model = User
        fields = ("username", "password", "email", "profile_img", "birthday")

    def create(self, validated_data):
        """회원가입 시 사용자가 보내는 JSON 형태의 데이터를 모델 객체의 형태로 역직렬화하는 메서드입니다."""
        user = super().create(validated_data)
        #print(validated_data)
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


class LoginSerializer(TokenObtainPairSerializer):
    """DRF의 JWT 로그인 방식에 사용되는 TokenObtainPairSerializer를 상속하여 Serializer를 커스터마이징하여 재정의합니다."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['username'] = user.username
        token['profile_img'] = user.profile_img.url
        
        return token

