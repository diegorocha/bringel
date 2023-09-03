from rest_framework.routers import DefaultRouter

from store.api.viewsets import TagViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet)
