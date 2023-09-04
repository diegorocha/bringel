from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from store.api.serializers import TagSerializer, SupplierSerializer, ProductSerializer, ProductVariantSerializer, \
    CustomerRatingSerializer, ProductDetailSerializer
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

    @swagger_auto_schema(operation_description="Return product with all related data",
                         responses={200: ProductDetailSerializer()})
    @action(detail=True, methods=['get'])
    def detailed(self, _, pk=None):
        product = self.get_object()
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)


class ProductVariantViewSet(ModelViewSet):
    serializer_class = ProductVariantSerializer
    queryset = ProductVariant.objects.all()


class CustomerRatingViewset(CreateModelMixin, GenericViewSet):
    serializer_class = CustomerRatingSerializer
    queryset = CustomerRating.objects.all()
