from django.contrib.auth import authenticate, get_user_model

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import (
    RegisterSerializer,
    LoginSerializer,
    TokenObtainPairSerializer,
)


class RegisterView(APIView):
    http_method_names = ["post"]

    permission_classes = (permissions.AllowAny,)  # 회원가입은 인증 필요없다

    def post(self, *args, **kwargs):
        serializer = RegisterSerializer(data=self.request.data)
        if serializer.is_valid():
            get_user_model().objects.create_user(**serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(
            status=status.HTTP_400_BAD_REQUEST, data={"errors": serializer.errors}
        )


class LoginView(generics.GenericAPIView):
    print("# login view start #")
    serializer_class = LoginSerializer

    def post(self, request):
        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        print(request.data)
        if user is not None:
            serializer = LoginSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            response = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            return response
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
