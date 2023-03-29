from django.contrib.auth import authenticate, get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as JwtTokenObtainPairSerializer,
)


class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD
    print(username_field)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "password",
        )


class LoginSerializer(serializers.Serializer):
    # username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True, write_only=True
    )  # write_only 옵션으로 클라 -> 서버 방향의 역직렬화 가능

    def validate(self, data):
        print("login serializer data: ", data)
        email = data.get("email")
        password = data.get("password")
        user = authenticate(email=email, password=password)
        print(f"email: {email}, password: {password}, user: {user}")
        if user:
            token = JwtTokenObtainPairSerializer.objects.get(user=user)
            # 토큰에 맞는 user 가져오기
            print(token)
            return token
        raise serializers.ValidationError(
            {"error": "Unable to log in with provided credentials!"}
        )
