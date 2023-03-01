from django.contrib.auth.models import User  # 장고의 기본 user 모델
from django.contrib.auth.password_validation import (
    validate_password,
)  # 장고의 기본 패스워드 검증도구
from rest_framework import serializers
from rest_framework.authtoken.models import Token  # Token 모델
from rest_framework.validators import UniqueValidator  # 이메일 중복 방지를 위한 검증도구


class RegisterSerializer(serializers.ModelSerializer):
    """회원가입 시리얼라이저"""

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],  # 이메일 중복 검증
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]  # password 검증
    )
    password2 = serializers.CharField(write_only=True, required=True)  # 비밀번호 확인 필드

    class Meta:
        """유저 모델에서 값을 받아와야할 필드"""

        model = User
        fields = ("username", "password", "password2", "email")

    def validate(self, data):
        """비밀번호 필드와 비밀번호 확인 필드의 값을 비교하여 비밀번호의 일치 여부를 판단"""
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return data

    def create(self, validated_data):
        """CREATE 요청에 대해 create 메소드 오버라이딩(유저랑 토큰 생성)"""
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        token = Token.objects.create(user=user)
        return user
