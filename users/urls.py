from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenRefreshView

app_name = "users"

urlpatterns = [
    path("register/", views.RegisterView.as_view()),  # POST: 회원가입
    path("login/", views.LoginView.as_view()),  # POST: 로그인
    path(
        "token/", views.EmailTokenObtainPairView.as_view()
    ),  # POST: email, password로 로그인(refresh, access 발급)
    path("token/refresh/", TokenRefreshView.as_view()),  # POST: refresh로 access 발급
]
