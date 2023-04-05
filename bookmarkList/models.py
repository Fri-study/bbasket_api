from django.db import models

from users.models import CustomAbstractUser

# Create your models here.
class BookmarkCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)  # 북마크 카테고리 이름
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    # SlugField: 사람이 읽을 수 있는 텍스트로 고유의 URL을 만듦 -> 카테고리는 포스트 개수보다 적을 것이고, 사용자가 인지할 수 있는 URL을 만드는 것이 좋을 것 같다고 판단
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"  # Categorys -> Categories 로 변경한 것


class Bookmark(models.Model):
    author = models.ForeignKey(
        CustomAbstractUser, on_delete=models.CASCADE, related_name="bookmarks"
    )  # 작성자, CustomAbstractBaseUser FK 연결
    title = models.CharField(max_length=200, null=False)  # 메모의 제목
    category = models.ForeignKey(
        BookmarkCategory, null=True, blank=True, on_delete=models.SET_NULL
    )  # 카테고리, FK 연결
    contents = models.TextField(blank=True)  # 메모 내용, 빈칸 허용
    link = models.TextField()  # 북마크 링크 필드
    thumbnail = models.ImageField(
        upload_to="images/"
    )  # 썸네일 필드 upload_to 이미치 파일이 저장될 위치! -> TODO: settings 편집
    created_at = models.DateTimeField(auto_now_add=True)  # 북마크 추가 날짜
    updated_at = models.DateTimeField(auto_now=True)  # 북마크 수정 날짜
    read = models.BooleanField(default=False)  # 읽었는지 안읽었는지, 읽었으면 True, 안읽었으면 False
