from django.urls import path
from rest_framework import routers

from .views import BookmarkListView

router = routers.SimpleRouter()
router.register("my-bookmark", BookmarkListView)

urlpatterns = router.urls
