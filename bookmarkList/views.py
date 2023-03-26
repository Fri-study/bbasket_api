from rest_framework import viewsets

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

    def perform_create(self, serializer):
        bookmark = Bookmark.objects.get(user=self.request.user)
        serializer.save(author=self.request.user, bookmark=Bookmark)
