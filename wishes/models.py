from django.db import models
from django.conf import settings


class Tag(models.Model):

    name = models.CharField(
        max_length=32, blank=True, null=True)


class Wish(models.Model):
    """
    - author : 작성자입니다.
        - 로그인 한 사용자를 자동으로 지정합니다.
    - wish_name(필수) : 위시 이름입니다.
    - content(필수) : 위시 내용입니다.
    - created_at : 위시가 작성된 일자 및 시간입니다.
        - 위시가 작성된 시간을 자동으로 저장하도록 설정합니다.
    - updated_at : 위시가 마지막으로 수정된 일자 및 시간입니다.
        - 위시를 수정할 때마다 자동으로 갱신되도록 설정합니다.
    - wish_img : 위시 이미지입니다.
    - likes : 위시를 좋아요 한 유저와의 관계입니다.
    - bookmarks : 위시를 북마크 한 유저와의 관계입니다.
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="작성자",
                               on_delete=models.SET_NULL, null=True, related_name="wishes")
    title = models.CharField("게시글 제목", max_length=50)
    wish_name = models.CharField("위시 상품명", max_length=50)
    content = models.TextField("내용")
    created_at = models.DateTimeField("생성 시각", auto_now_add=True)
    updated_at = models.DateTimeField("수정 시각", auto_now=True)
    # wish_img = models.ImageField("위시 이미지", blank=True, null=True, upload_to='wish/wish_img/%Y%M%D/')
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name="좋아요", related_name="likes")
    bookmarks = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name="북마크", related_name="bookmarks")
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return str(self.title)

# 이미지 업로드 경로


def image_upload_path(instance, filename):
    return f'wish/wish_img/{instance.wish.id}/{filename}'


class WishImage(models.Model):
    wish = models.ForeignKey(
        Wish, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to=image_upload_path, default='images/DefaultThumbnail.png')

    class Meta:
        db_table = 'wish_image'

class Comment(models.Model):
    """
    - author(필수) : 댓글의 작성자입니다.
        - 사용자의 고유값을 입력받아 지정합니다.
    - article(필수) : 댓글을 작성할 게시글입니다.
        - 게시글의 고유값을 입력받아 지정합니다.
    - content(필수) : 댓글 내용입니다.
    - created_at : 댓글이 작성된 일자 및 시간입니다.
        - 댓글이 작성된 시간을 자동으로 저장하도록 설정합니다.
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="댓글 작성자", on_delete=models.SET_NULL, null=True)
    wish = models.ForeignKey(Wish, verbose_name="위시",
                             on_delete=models.CASCADE, related_name="comments")
    content = models.TextField("댓글 내용")
    created_at = models.DateTimeField("댓글 생성 시각", auto_now_add=True)

    def __str__(self):
        return str(self.content)
