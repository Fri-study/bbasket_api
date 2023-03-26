from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)


class CustomAbstractBaseUser(AbstractBaseUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)  # 로그인에 사용, 중복되면 안되는 값
    password = models.CharField(max_length=50)  # 패스워드 필드를 forms.py 에 정의함
    password2 = models.CharField(max_length=50)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
