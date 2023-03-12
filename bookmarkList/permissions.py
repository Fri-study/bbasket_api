from rest_framework import permissions


class CustomReadOnly(permissions.BasePermission):
    # 조회는 누구나 가능, 편집은 로그인+글 작성자
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.auther == request.user
