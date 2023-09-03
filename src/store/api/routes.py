from rest_framework.routers import DefaultRouter

from store.api.viewsets import TagViewSet, SupplierViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'suppliers', SupplierViewSet)
