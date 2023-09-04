from rest_framework.fields import ReadOnlyField, CharField, FloatField
from rest_framework.relations import SlugRelatedField, StringRelatedField, PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from store.models import Tag, Supplier, ProductVariant, Product


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'description']


class SupplierSerializer(ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name']


class ProductVariantSerializer(ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'variant_name', 'variant_value', 'sku', 'in_stock', 'price']


class ProductVariantNestedSerializer(ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'variant_name', 'variant_value', 'sku', 'in_stock', 'price']


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'supplier', 'name', 'description', 'tags', 'rating', 'variants']
    supplier = SlugRelatedField(slug_field='name', queryset=Supplier.objects.all())
    tags = SlugRelatedField(slug_field='name', many=True, queryset=Tag.objects.all())
    rating = FloatField(read_only=True)
    variants = ProductVariantNestedSerializer(many=True, read_only=True)
