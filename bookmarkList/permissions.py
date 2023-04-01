from rest_framework import permissions


class CustomReadOnly(permissions.BasePermission):
    # 유저 개인 페이지이므로 로그인한 본인만 접속 가능해야 함 -> 로그인하지 않은 사용자의 접근 막음
    # TODO: 로그인한 본인의 접속이 정상적으로 되는지
    def has_permission(self, request, view):
        if request.method == "GET":
            return False
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.auther == request.user
