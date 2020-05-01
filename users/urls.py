from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("log_in", views.LoginView.as_view(), name="login"),
    path("log_in/github", views.github_login, name="github-login"),
    path("log_in/github/callback", views.github_callback, name="github-callback"),
    path("log_in/kakao", views.kakao_login, name="kakao-login"),
    path("log_in/kakao/callback", views.kakao_callback, name="kakao-callback"),
    # path("log_in/google", views.google_login, name="google-login"),
    # path("log_in/google/callback", views.google_callback, name="google-callback"),
    path("log_in/naver", views.naver_login, name="naver-login"),
    path("log_in/naver/callback", views.naver_callback, name="naver-callback"),
    path("logout", views.user_logout, name="logout"),
    path("signup", views.SignUpView.as_view(), name="signup"),
    path("verify/<str:key>", views.complete_verification, name="complete-verification"),
]
