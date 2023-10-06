from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from users.models import User
from rest_framework.generics import get_object_or_404 
from users.serializers import ProfileSerializer, UserSerializer

        
class ProfileView(APIView):
    # permission_class = [permissions.IsAuthenticated]    # 로그인된 유저만 회원정보 조회 및 수정 가능

    def get(self, request, user_id):
        """사용자의 프로필을 받아 보여줍니다."""
        profile = get_object_or_404(User, id=user_id)
        if request.user.email == profile.email:                
            serializer = ProfileSerializer(profile)    
            return Response(serializer.data, status=status.HTTP_200_OK) 
        else:
            return Response({"message":serializer.errors}, status=status.HTTP_403_FORBIDDEN)

class SignupView(APIView):
    def post(self, request):
        """사용자 정보를 받아 회원가입합니다."""
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"회원가입 성공!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)