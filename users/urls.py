from django.urls import path
from users import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='sign_up_view'),
    path('login/', views.LoginView.as_view(), name='login_view'),
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='profile_view'),
    path('follow/<str:user_username>/', views.FollowView.as_view(), name='follow_view'),
    path('verify-email/<str:uidb64>/<str:token>/', views.EmailVerificationView.as_view(), name='verify_email'),
    path('test/', views.Test.as_view()),
    path('<str:user_username>/feed/', views.FeedView.as_view(), name='feed_view'),
    path('<str:user_username>/mypage/', views.MyPageView.as_view(), name='my_page_view'),
]
