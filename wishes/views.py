from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from wishes.serializers import WishSerializer, WishCreateSerializer, WishListSerializer

from wishes.models import Wish, Comment

class WishView(APIView):
    def get(self, request, wish_id=None):
        """
        wish_id를 받아 특정 게시물을 Response 합니다. (Read : Wish Detail Page)
        wish_id가 없을 경우 모든 게시물을 Response 합니다. (Main Page)
        """
        if wish_id == None:
            """ 모든 게시물 List를 반환합니다. """
            wishes = Wish.objects.all()
            serializer = WishListSerializer(wishes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            """ 특정 게시물을 반환합니다. """
            wish = get_object_or_404(Wish, id=wish_id)
            serializer = WishSerializer(wish)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        
    def post(self, request):
        """위시 정보를 받아 위시를 생성합니다."""
        # print(request.META)
        # print(request.META.get("HTTP_AUTHORIZATION"))
        # print(request.FILES)
        if not request.user.is_authenticated :
            return Response({"message":"로그인 해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = WishCreateSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                                
    def put(self, request, wish_id):
        """수정된 위시 정보를 받아 위시를 수정합니다."""
        wish = get_object_or_404(Wish, id=wish_id)
        if request.user == wish.author:
            serializer = WishCreateSerializer(wish, data=request.data, context={'request': request}) # 수정 시 필요한 모든 필드가 채워진 상태로 전달될 것이라 판단 -> partial=True 넣지 않음.
            if serializer.is_valid():
                serializer.save() # 여기는 이미 기존 article에 author가 저장되어있어서 따로 request.user를 안 해줘도 됨.
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