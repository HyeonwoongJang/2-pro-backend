from django.urls import path
from wishes import views


urlpatterns = [
    path('', views.WishView.as_view(), name='wish_view'),
    path('<int:wish_id>/', views.WishView.as_view(), name='wish_detail_view'),
    # path('feed/', views.FeedView.as_view(), name='feed_view'),
    path('<int:wish_id>/comment/', views.CommentView.as_view(),
         name='comment_create_view'),
    path('<int:wish_id>/comment/<int:comment_id>/',
         views.CommentView.as_view(), name='comment_delete_view'),
    path('<int:wish_id>/like/', views.LikeView.as_view(), name='like_view'),
    path('<int:wish_id>/bookmark/',
         views.BookmarkView.as_view(), name='bookmark_view'),
]
