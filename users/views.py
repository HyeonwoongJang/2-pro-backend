from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from user.models import User

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
        """사용자가 다른 사용자를 팔로우하고 언팔로우합니다."""

        # user_id 사용해서 팔로우 사용자 가져오기
        followee = get_object_or_404(User, id=user_id)
        follower = request.user  # 팔로우 요청을 보내는 사용자
        if follower in follower.followers.all():  # 사용자를 이미 팔로우한다면
            # followee 사용자 목록에서 follower remove로 제거하기
            followee.followers.remove(follower)
            return Response("unfollow 했습니다.", status=status.HTTP_200_OK)
        else:
            # 아니면 followee 사용자 목록에 follower 추가
            followee.followers.add(follower)
            return Response("follow 했습니다.", status=status.HTTP_200_OK)
