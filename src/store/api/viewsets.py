from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from store.api.serializers import TagSerializer, SupplierSerializer, ProductSerializer, ProductVariantSerializer, \
    CustomerRatingSerializer
from store.models import Tag, Supplier, Product, ProductVariant, CustomerRating


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


class CustomerRatingViewset(CreateModelMixin, GenericViewSet):
    serializer_class = CustomerRatingSerializer
    queryset = CustomerRating.objects.all()
