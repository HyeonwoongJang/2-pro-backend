from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from users.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import LoginSerializer, ProfileSerializer, UserSerializer

# 새로운 사용자를 생성한 후에 이메일 확인 토큰을 생성하고 사용자 모델에 저장합니다. 이메일 인증 링크를 사용자의 이메일 주소로 전송합니다.
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail

from django.utils.encoding import force_str

class EmailVerificationView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                # 사용자 모델의 email_verified 필드를 True로 설정
                user.email_verified = True
                user.save()
                return Response({"message": "이메일 확인이 완료되었습니다."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "이메일 확인 링크가 잘못되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "사용자를 찾을 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    def post(self, request):
        """사용자 정보를 받아 회원가입합니다."""

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # 이메일 확인 토큰 생성
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # 이메일에 확인 링크 포함하여 보내기
            verification_url = f"http://127.0.0.1:8000/users/verify-email/{uid}/{token}/"
            # 이메일 전송 코드 작성 및 이메일에 verification_url을 포함하여 보내기

            # 이메일 전송
            subject = '이메일 확인 링크'
            message = f'이메일 확인을 완료하려면 다음 링크를 클릭하세요: {verification_url}'
            from_email = 'estherwoo01@gmail.com'
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list)

            return Response({"message": "회원가입 성공! 이메일을 확인하세요."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    def get(self, request, user_id):
        """사용자의 프로필을 받아 보여줍니다."""
        profile = get_object_or_404(User, id=user_id)
        if request.user.email == profile.email:                
            serializer = ProfileSerializer(profile)    
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        
    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        

class LoginView(TokenObtainPairView):
    """
    사용자의 정보를 받아 로그인합니다.
    DRF의 JWT 토큰 인증 로그인 방식에 기본 제공되는 클래스 뷰를 커스터마이징하여 재정의합니다.
    """
    serializer_class = LoginSerializer


class FollowView(APIView):
    def post(self, request, user_id):
        """사용자가 다른 사용자를 팔로우하고 언팔로우합니다."""

        # user_id 사용해서 팔로우 사용자 가져오기
        user = get_object_or_404(User, id=user_id)
        me = request.user  # 팔로우 요청을 보내는 사용자
        if me in user.followers.all():  # 사용자를 이미 팔로우한다면
            # followee 사용자 목록에서 follower remove로 제거하기
            user.followers.remove(me)
            return Response("unfollow 했습니다.", status=status.HTTP_200_OK)
        else:
            # 아니면 followee 사용자 목록에 follower 추가
            user.followers.add(me)
            return Response("follow 했습니다.", status=status.HTTP_200_OK)