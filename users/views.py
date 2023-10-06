from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from users.models import User
from users.serializers import UserSerializer


class SignupView(APIView):
    def post(self, request):
        """사용자 정보를 받아 회원가입합니다."""

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입 성공!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class FollowView(APIView):
    def post(self, request, user_id):
        """사용자는 다를 사용자를 팔로우하거나 언팔로우하는 기능입니다."""
        follower = get_object_or_404(User, id=user_id)
        followee = request.user
        if followee in follower.followers.all():
            follower.followers.remove(followee)
            return Response("언팔로우 했습니다.", status=status.HTTP_200_OK)
        else:
            follower.followers.add(followee)
            return Response("팔로우 했습니다.", status=status.HTTP_200_OK)
