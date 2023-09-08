from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from store.api.permissions import UserReadsAdminWrites
from store.api.serializers import TagSerializer, SupplierSerializer, ProductSerializer, ProductVariantSerializer, \
    CustomerRatingSerializer, ProductDetailSerializer
from store.models import Tag, Supplier, Product, ProductVariant, CustomerRating


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    filterset_fields = ['name']
    permission_classes = [AllowAny]  # Allow anonymoys users


class SupplierViewSet(ModelViewSet):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
    filterset_fields = ['name']
    permission_classes = [UserReadsAdminWrites]


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filterset_fields = ['supplier', 'tags']
    permission_classes = [UserReadsAdminWrites]

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
    filterset_fields = ['product', 'variant_name', 'variant_value', 'in_stock']
    permission_classes = [UserReadsAdminWrites]


class CustomerRatingViewset(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = CustomerRatingSerializer
    queryset = CustomerRating.objects.all()
    filterset_fields = ['product']
    permission_classes = [IsAuthenticated]
