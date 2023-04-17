from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Bookmark
from .permissions import CustomReadOnly
from .serializers import BookmarkListSerializer, BookmarkCreateSerializer

# Create your views here.

class BookmarkListView(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    permission_classes = [CustomReadOnly]

    def get_serializer_class(self):
        if self.action == "list" or "retrieve":
            return BookmarkListSerializer
        return BookmarkCreateSerializer
        # Serializer: 데이터 검증하고, 유효한 경우 데이터를 생성

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
