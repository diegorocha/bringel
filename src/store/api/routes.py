from rest_framework.routers import DefaultRouter

from store.api.viewsets import TagViewSet, SupplierViewSet, ProductViewSet, ProductVariantViewSet, CustomerRatingViewset

router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'products/variants', ProductVariantViewSet)
router.register(r'products/rating', CustomerRatingViewset)
router.register(r'products', ProductViewSet)
