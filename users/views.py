from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from users.models import User
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import UserSerializer, LoginSerializer

class SignupView(APIView):
    def post(self, request):
        """사용자 정보를 받아 회원가입합니다."""
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"회원가입 성공!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)
        

class LoginView(TokenObtainPairView):
    """
    사용자의 정보를 받아 로그인합니다.
    DRF의 JWT 토큰 인증 로그인 방식에 기본 제공되는 클래스 뷰를 커스터마이징하여 재정의합니다.
    """
    serializer_class = LoginSerializer
