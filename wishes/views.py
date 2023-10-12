from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from wishes.serializers import WishSerializer, WishCreateSerializer, WishListSerializer, CommentSerializer

from wishes.models import Wish, Comment
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination


class WishView(ListAPIView):
    # APIView에서는 pagination 지원하지 않음(paginate_queryset찾을수없음)
    queryset = Wish.objects.all().order_by('-created_at')
    serializer_class = WishListSerializer
    pagination_class = PageNumberPagination
    # 쿼리셋으로 게시글 목록을 최신순으로 가져오고 페이지네이션 활성화(settings.py에 페이지당 게시글항목 설정가능)

    def retrieve(self, request, *args, **kwargs):
        # retrieve=개별 객체의 상세 정보를 가져오는 역할, #args(매개변수를 튜플로 모을 때) #kwargs(매개변수를 딕셔너리로 모을 때)
        wish_id = self.kwargs.get('wish_id')
        if wish_id is not None:
            wish = get_object_or_404(Wish, id=wish_id)
            serializer = WishSerializer(wish)
            return Response(serializer.data, status=status.HTTP_200_OK)



# class WishView(APIView):
#     def get(self, request, wish_id=None):
#         """
#         wish_id를 받아 특정 게시물을 Response 합니다. (Read : Wish Detail Page)
#         wish_id가 없을 경우 모든 게시물을 Response 합니다. (Main Page)
#         """
#         if wish_id == None:
#             """ 모든 게시물 List를 반환합니다. """
#             wishes = Wish.objects.all().order_by('-created_at')
#             serializer = WishListSerializer(wishes, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#                 """ 특정 게시물을 반환합니다. """
#                 wish = get_object_or_404(Wish, id=wish_id)
#                 serializer = WishSerializer(wish)
#                 return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """위시 정보를 받아 위시를 생성합니다."""
        # print(request.META)
        # print(request.META.get("HTTP_AUTHORIZATION"))
        # print(request.FILES)
        if not request.user.is_authenticated:
            return Response({"message": "로그인 해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = WishCreateSerializer(
                data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, wish_id):
        """수정된 위시 정보를 받아 위시를 수정합니다."""
        wish = get_object_or_404(Wish, id=wish_id)
        if request.user == wish.author:
            # 수정 시 필요한 모든 필드가 채워진 상태로 전달될 것이라 판단 -> partial=True 넣지 않음.
            serializer = WishCreateSerializer(
                wish, data=request.data, context={'request': request})
            if serializer.is_valid():
                # 여기는 이미 기존 article에 author가 저장되어있어서 따로 request.user를 안 해줘도 됨.
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, wish_id):
        """지정된 위시를 삭제합니다."""
        wish = get_object_or_404(Wish, id=wish_id)
        if request.user == wish.author:
            wish.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)


class CommentView(APIView):
    def get(self, request, wish_id):
        comments = Comment.objects.filter(
            wish_id=wish_id).order_by("-created_at")
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, wish_id):
        """wish_id를 받아 해당 위시에 댓글을 생성합니다."""
        if request.user.is_authenticated:
            serialzer = CommentSerializer(data=request.data)
            if serialzer.is_valid():
                serialzer.save(author=request.user, wish_id=wish_id)
                return Response(serialzer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, wish_id, comment_id):
        """지정된 댓글을 삭제합니다."""
        comment = get_object_or_404(Comment, id=comment_id)
        # print(comment)
        if request.user.is_authenticated:
            if not request.user == comment.author:
                return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
            else:
                comment.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)


class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, wish_id):
        """like / unlike 기능입니다."""
        wish = Wish.objects.get(id=wish_id)
        me = request.user
        if me in wish.likes.all():
            wish.likes.remove(me)
            return Response("unlike 했습니다.", status=status.HTTP_200_OK)
        else:
            wish.likes.add(me)
            return Response("like 했습니다.", status=status.HTTP_200_OK)


class BookmarkView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, wish_id):
        """bookmark / unbookmark 기능입니다."""
        wish = Wish.objects.get(id=wish_id)
        me = request.user
        if me in wish.bookmarks.all():
            wish.bookmarks.remove(me)
            return Response("unbookmark 했습니다.", status=status.HTTP_200_OK)
        else:
            wish.bookmarks.add(me)
            return Response("bookmark 했습니다.", status=status.HTTP_200_OK)
