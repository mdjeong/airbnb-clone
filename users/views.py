# Standard Libraries
import os
import json

# Third-party Libraries
from oauthlib.oauth2 import WebApplicationClient
import requests
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Internal Import
from . import forms, models

NAVER_CLIENT_ID = os.environ.get("NAVER_ID", None)
NAVER_CLIENT_SECRET = os.environ.get("NAVER_SECRET", None)
NAVER_CLIENT = WebApplicationClient(NAVER_CLIENT_ID)

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_SECRET", None)
GOOGLE_CLIENT = WebApplicationClient(GOOGLE_CLIENT_ID)


class LoginView(View):
    def get(self, request):
        form = forms.LoginForm(initial={"email": "mdhyunjin@gmail.com"})
        return render(request, "users/login.html", context={"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))

        return render(request, "users/login.html", context={"form": form})


"""
class LoginFormView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
"""


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpModelForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "hyunjin",
        "last_name": "jeong",
        "email": "mdhyunjin@gmail.com",
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def user_logout(request):
    logout(request)
    return redirect(reverse("core:home"))


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add success message
    except models.User.DoesNotExit:
        # to do: add error message
        pass

    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/log_in/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        code = request.GET.get("code", None)
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException("Can't get access token from github")
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method == models.User.LOGIN_GITHUB:
                            login(request, user)
                        else:
                            raise GithubException(
                                f"Please, Login with {user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException()
        else:
            raise GithubException("Can't get code for token from github.com")
    except GithubException as e:
        messages.error(request, e)
        print(e)
        return redirect(reverse("users:login"))


class KakaoException(Exception):
    pass


def kakao_login(request):
    app_key = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/log_in/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_key}&redirect_uri={redirect_uri}&response_type=code"
    )


def kakao_callback(request):
    try:
        code = request.GET.get("code", None)
        app_key = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/log_in/kakao/callback"
        if code is not None:
            print(f"success to receive the code: {code}")
            token_request = requests.get(
                f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_key}&redirect_uri={redirect_uri}&code={code}",
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise KakaoException("Can't Get access token from kakao")

            access_token = token_json.get("access_token")
            print(f"success to receive the access token: {access_token}")
            profile_request = requests.get(
                f"https://kapi.kakao.com/v2/user/me?",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            profile_json = profile_request.json()
            print(profile_json)
            email = profile_json.get("kakako_account.email")
            if email is None:
                raise KakaoException()
            properties = profile_json.get("properties")
            nickname = properties.get("nickname")
            profile_image = properties.get("profile_image")
            try:
                user = models.User.objects.get(email=email)
                if user.login_method != models.User.LOGIN_KAKAO:
                    raise KakaoException
                user.avatar = profile_image
                user.save()
            except models.User.DoesNotExist:
                user = models.User.objects.create(
                    email=email,
                    first_name=nickname,
                    login_method=models.User.LOGIN_KAKAO,
                    email_verified=True,
                    avatar=profile_image,
                )
                user.set_unusable_password()
                user.save()
            login(request, user)

        else:
            raise KakaoException("Can't Get Authorized Code from Kakao Login")
        return redirect(reverse("users:login"))
    except KakaoException as e:
        messages.error(request, e)
        print(e)
        return redirect(reverse("users:login"))


class NaverException(Exception):
    pass


def naver_login(request):
    authorization_endpoint = "https://nid.naver.com/oauth2.0/authorize"
    request_uri = NAVER_CLIENT.prepare_request_uri(
        authorization_endpoint,
        redirect_uri="http://127.0.0.1:8000/users/log_in/naver/callback",
        scope=["id", "name", "email", "profile_image"],
    )
    print(f"request_uri for code: {request_uri}")
    return redirect(request_uri)


def naver_callback(request):
    try:
        code = request.GET.get("code", None)
        token_endpoint = "https://nid.naver.com/oauth2.0/token"

        # prepare and send a request to get tokens!
        token_url, headers, body = NAVER_CLIENT.prepare_token_request(
            token_endpoint,
            authorization_response=request.get_full_path(),
            redirect_url=request.get_full_path(),
            code=code,
        )
        print(f"token_url: {token_url}\nheaders: {headers}")
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(NAVER_CLIENT_ID, NAVER_CLIENT_SECRET),
        )
        print(f"token_response: {token_response}\njson: {token_response.json()}")
        # Parse the tokens!
        NAVER_CLIENT.parse_request_body_response(json.dumps(token_response.json()))
        userinfo_endpoint = "https://openapi.naver.com/v1/nid/me"
        uri, headers, body = NAVER_CLIENT.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        print(
            f"userinfo_response: {userinfo_response}\njson: {userinfo_response.json()}"
        )

        # You want to make sure their email is verified.
        # the user authenticated with Google, authroized your
        # app, and now you've verified their email through Google!
        if userinfo_response.json()["response"]["email"]:
            users_email = userinfo_response.json()["response"]["email"]
            picture = userinfo_response.json()["response"]["profile_image"]
            users_name = userinfo_response.json()["response"]["name"]
        else:
            raise NaverException("No Data From Naver")

        try:
            user = models.User.objects.get(email=users_email)
            if user.login_method != models.User.LOGIN_NAVER:
                raise NaverException
            user.avatar = picture
            user.save()
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=users_email,
                first_name=users_name,
                login_method=models.User.LOGIN_NAVER,
                email_verified=True,
                avatar=picture,
            )
            user.set_unusable_password()
            user.save()
        # Begin user session by logging the user in
        login(request, user)
        return redirect(reverse("users:login"))
    except NaverException as e:
        messages.error(request, e)
        print(e)
        return redirect(reverse("users:login"))

    # # Send user back to homepage
    # return redirect(reverse("core:home"))
