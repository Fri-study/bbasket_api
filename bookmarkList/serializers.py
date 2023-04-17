from rest_framework import serializers

from .models import Bookmark


class BookmarkListSerializer(serializers.ModelSerializer):
    """유저 메인 보드에 사용자의 북마크 출력"""

    class Meta:
        model = Bookmark
        fields = ("title", "thumbnail", "link")

class BookmarkCreateSerializer(serializers.ModelSerializer):
    """임시 시리얼라이저 테스트용!! 북마크 생성 시리얼 라이저"""
    class Meta:
        model = Bookmark
        fields = ("title", "category", "contents", "link", "thumbnail", "read")

    def create(self, validated_data):
        author = self.context['request'].user
        bookmark_instance = Bookmark.objects.create(author=author, **validated_data)
        return bookmark_instance