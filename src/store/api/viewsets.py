from rest_framework.viewsets import ModelViewSet

from store.api.serializers import TagSerializer, SupplierSerializer, ProductSerializer, ProductVariantSerializer
from store.models import Tag, Supplier, Product, ProductVariant


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class SupplierViewSet(ModelViewSet):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductVariantViewSet(ModelViewSet):
    serializer_class = ProductVariantSerializer
    queryset = ProductVariant.objects.all()
