from rest_framework.serializers import ModelSerializer

from store.models import Tag, Supplier


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'description']


class SupplierSerializer(ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name']
