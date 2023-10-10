from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


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
        validators=[UniqueValidator(
            queryset=User.objects.all(), message="해당 이메일은 이미 사용중입니다.",)]
    )

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(), message="해당 유저이름은 이미 사용중입니다.")]
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

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['username'] = user.username
        token['profile_img'] = user.profile_img.url

        return token
