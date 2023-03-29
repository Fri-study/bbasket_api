from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        UserModel = get_user_model()
        try:
            email = kwargs.get("email", None)
            if email is None:
                # admin 페이지에서 createsuperuser로 만든 계정으로 로그인 하는 경우에 'username' 에 email 값이 들어오기 때문에,
                # email이 None인 경우 'username' 값을 email 변수에 저장하도록 따로 처리해야 한다.
                email = kwargs.get("username", None)

            user = UserModel.objects.get(email=email)
            if user.check_password(kwargs.get("password", None)):
                return user

        except UserModel.DoesNotExist:
            return None
        return None
