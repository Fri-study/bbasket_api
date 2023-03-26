from django.contrib.auth import (
    authenticate,
)  # 장고 기본 authenticate 함수 -> TokenAuth 방식으로 인증해 줌
from django.contrib.auth.password_validation import (
    validate_password,
)  # 장고의 기본 패스워드 검증도구
from rest_framework import serializers
from rest_framework.authtoken.models import Token  # Token 모델
from rest_framework.validators import UniqueValidator  # 이메일 중복 방지를 위한 검증도구

from .models import CustomUserManager, CustomAbstractBaseUser


class RegisterSerializer(serializers.ModelSerializer):
    """회원가입 시리얼라이저"""

    print("## RegisterSerializer Start ##")
    # email = serializers.CharField(required=True)
    #
    # password = serializers.CharField(
    #     required=True,
    #     write_only=True,
    #     validators=[validate_password]
    # )
    # password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        """유저 모델에서 값을 받아와야할 필드"""

        model = CustomAbstractBaseUser
        fields = (
            "username",
            "password",
            "password2",
            "email",
        )
        # 아래의 부분은 https://stackoverflow.com/questions/66030271/uniquevalidator-in-drf 참고
        extra_kwargs = {
            "email": {
                "validators": [
                    UniqueValidator(queryset=CustomAbstractBaseUser.objects.all()),
                ],
            },
            "password": {"validators": [validate_password], "write_only": True},
            "password2": {"write_only": True},
        }

    def validate(self, data):
        """비밀번호 필드와 비밀번호 확인 필드의 값을 비교하여 비밀번호의 일치 여부를 판단"""
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return data

    def create(self, validated_data):
        """CREATE 요청에 대해 create 메소드 오버라이딩(유저랑 토큰 생성)"""
        # user = User.objects.create_user(
        #     email=validated_data["email"],
        #     username=validated_data["username"]
        # )
        user = CustomUserManager.create_user(email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        token = Token.objects.create(user=user)
        return user


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
            token = Token.objects.get(user=user)  # 토큰에 맞는 user 가져오기
            return token
        raise serializers.ValidationError(
            {"error": "Unable to log in with provided credentials!"}
        )
