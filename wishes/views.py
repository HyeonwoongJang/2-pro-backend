from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from wishes.serializers import WishCreateSerializer, WishSerializer
from wishes.models import Wish


class WishView(APIView):
    def get(self, request, wish_id=None):
        if wish_id is None:
            wishes = Wish.objects.all()
            serializer = WishSerializer(wishes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            wish = Wish.objects.get(id=wish_id)
            serializer = WishSerializer(wish)
            return Response(serializer.data, status=status.HTTP_200_OK)
        """
        wish_id를 받아 특정 게시물을 Response 합니다. (Read : Wish Detail Page)
        wish_id가 없을 경우 모든 게시물을 Response 합니다. (Main Page)
        """

    def post(self, request):
        """위시 정보를 받아 위시를 생성합니다."""
        if not request.user.is_authenticated:
            return Response({"message": "로그인 해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = WishCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, wish_id):
        """수정된 위시 정보를 받아 위시를 수정합니다."""

    def delete(self, request, wish_id):
        """지정된 위시를 삭제합니다."""


class CommentView(APIView):
    def post(self, request, wish_id):
        """wish_id를 받아 해당 위시에 댓글을 생성합니다."""

    def delete(self, request, comment_id):
        """지정된 댓글을 삭제합니다."""


class LikeView(APIView):
    def post(self, request, wish_id):
        """like / unlike 기능입니다."""


class BookmarkView(APIView):
    def post(self, request, wish_id):
        """bookmark / unbookmark 기능입니다."""
