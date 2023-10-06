from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.serializers import UserSerializer

class SignupView(APIView):
    def post(self, request):
        """사용자 정보를 받아 회원가입합니다."""
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"회원가입 성공!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":serializer.erorrs}, status=status.HTTP_400_BAD_REQUEST)