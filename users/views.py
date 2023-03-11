# from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import LoginSerializer, RegisterSerializer

from .models import CustomAbstractBaseUser


class RegisterView(generics.CreateAPIView):
    """CreateAPIView(generics) 사용"""

    print("## RegisterView Start ##")
    queryset = CustomAbstractBaseUser.objects.all()
    serializer_class = RegisterSerializer
    print("## RegisterView End ##")


class LoginView(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):
        print("login view request data: ", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data  # validate()의 리터값인 Token을 받아옴
        return Response({"token": token.key}, status=status.HTTP_200_OK)
