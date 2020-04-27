from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("log_in", views.LoginView.as_view(), name="login"),
    path("log_in/github", views.github_login, name="github-login"),
    path("log_in/github/callback", views.github_callback, name="github-callback"),
    path("logout", views.user_logout, name="logout"),
    path("signup", views.SignUpView.as_view(), name="signup"),
    path("verify/<str:key>", views.complete_verification, name="complete-verification"),
]
