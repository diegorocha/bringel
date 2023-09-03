from rest_framework.viewsets import ModelViewSet

from store.api.serializers import TagSerializer, SupplierSerializer
from store.models import Tag, Supplier


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class SupplierViewSet(ModelViewSet):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
