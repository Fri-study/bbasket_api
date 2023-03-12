from django.contrib import admin
from .models import BookmarkCategory, Bookmark

# Register your models here.
admin.site.register(Bookmark)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    # category name 이 입력되면 자동으로 slug 가 생성됨! -> admin 사이트에서 확인 가능


admin.site.register(BookmarkCategory, CategoryAdmin)

# admin 페이지 접속 방법: 127.0.0.1/admin 으로 접속
# super user 계정 정보: bookmarkadmin / v1q2w3e!!

# 백엔드에서 db 삭제하게 되면 계정 모두 삭제됩니다! 혹시 접속이 안될 경우엔 문의 주세요!
