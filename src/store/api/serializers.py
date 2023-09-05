from drf_yasg.utils import swagger_serializer_method
from rest_framework.fields import CharField, FloatField, IntegerField, BooleanField, DecimalField, DateTimeField, \
    SerializerMethodField
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from store.models import Tag, Supplier, ProductVariant, Product, CustomerRating, PriceHistory


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'description']
    id = IntegerField(label='Id', help_text='Tag ID', read_only=True)
    name = CharField(label='Name', help_text='Tag name', max_length=50, required=True,
                     validators=[UniqueValidator(queryset=Tag.objects.all())])
    description = CharField(label='Description', help_text='Tag description', max_length=100, required=False)


class SupplierSerializer(ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name']
    id = IntegerField(label='Id', help_text='Supplier ID', read_only=True)
    name = CharField(label='Name', help_text='Supplier name', max_length=100, required=True,
                     validators=[UniqueValidator(queryset=Supplier.objects.all())])


class PriceHistorySerializer(ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ['price', 'updated_at']

    price = DecimalField(label='Price', max_digits=8, decimal_places=2, read_only=True)
    updated_at = DateTimeField(label='Updated At', read_only=True)


class ProductVariantSerializer(ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'variant_name', 'variant_value', 'sku', 'in_stock', 'price', 'price_history']

    id = IntegerField(label='Id', help_text='ProductVariant ID', read_only=True)
    product = PrimaryKeyRelatedField(label='Product', help_text='Product ID', queryset=Product.objects.all(),
                                     required=True)
    variant_name = CharField(label='Variant Name', help_text='Name of variant', max_length=20, required=True)
    variant_value = CharField(label='Variant Value', help_text='Value of variant', max_length=50, required=True)
    sku = CharField(label='SKU', help_text='SKU code', max_length=8, required=True,
                    validators=[UniqueValidator(queryset=ProductVariant.objects.all())])
    in_stock = BooleanField(label='In Stock', help_text='', default=False)
    price = DecimalField(label='Price', max_digits=8, decimal_places=2, required=True)
    price_history = SerializerMethodField(label='Price History', read_only=True)

    @swagger_serializer_method(serializer_or_field=PriceHistorySerializer(many=True))
    def get_price_history(self, instance):
        query = instance.price_history.all()[:10]  # Only show last 10 prices
        serializer = PriceHistorySerializer(query, many=True)
        return serializer.data


class ProductVariantNestedSerializer(ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'variant_name', 'variant_value', 'sku', 'in_stock', 'price']
        ref_name = 'ProductVariantRead'
    id = IntegerField(label='Id', help_text='ProductVariant ID', read_only=True)
    variant_name = CharField(label='Variant Name', help_text='Name of variant', max_length=20, required=True)
    variant_value = CharField(label='Variant Value', help_text='Value of variant', max_length=50, required=True)
    sku = CharField(label='SKU', help_text='SKU code', max_length=8, required=True)
    in_stock = BooleanField(label='In Stock', help_text='', default=False)
    price = DecimalField(label='Price', max_digits=8, decimal_places=2, required=True)


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'supplier', 'name', 'description', 'tags', 'rating', 'variants']
    supplier = SlugRelatedField(slug_field='name', help_text='Supplier Name',  queryset=Supplier.objects.all())
    tags = SlugRelatedField(slug_field='name', help_text='Tag Name',  many=True, queryset=Tag.objects.all())
    rating = FloatField(help_text='Calculated rating', read_only=True)
    variants = ProductVariantNestedSerializer(many=True, read_only=True)


class CustomerRatingSerializer(ModelSerializer):
    class Meta:
        model = CustomerRating
        fields = ['product', 'rating', 'description', 'created_at']
    product = PrimaryKeyRelatedField(label='Product', help_text='Product ID', queryset=Product.objects.all(),
                                     required=True)
    rating = IntegerField(help_text='Rating from 1 to 5',  min_value=1, max_value=5)


class CustomerRatingReadSerializer(ModelSerializer):
    class Meta:
        model = CustomerRating
        fields = ['rating', 'description', 'created_at']
    rating = IntegerField(help_text='Rating from 1 to 5', min_value=1, max_value=5)


class ProductDetailSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'supplier', 'name', 'description', 'tags', 'rating', 'ratings', 'variants']
        ref_name = 'DetailedProduct'
    supplier = SlugRelatedField(slug_field='name', help_text='Supplier Name', queryset=Supplier.objects.all())
    tags = SlugRelatedField(slug_field='name', help_text='Tag Name', many=True, queryset=Tag.objects.all())
    rating = FloatField(help_text='Calculated rating', min_value=1, max_value=5, read_only=True)
    variants = ProductVariantNestedSerializer(many=True, read_only=True)
    ratings = CustomerRatingReadSerializer(many=True)
