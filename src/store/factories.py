from factory import SubFactory, post_generation
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger, FuzzyDecimal, FuzzyText

from store.models import CustomerRating, Tag, Supplier, Product, ProductVariant, PriceHistory


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag
    name = FuzzyText()


class SupplierFactory(DjangoModelFactory):
    class Meta:
        model = Supplier
    name = FuzzyText()


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product
    supplier = SubFactory(SupplierFactory)
    name = FuzzyText()
    description = FuzzyText()

    @post_generation
    def tags(self, create, extracted, **kwargs):
        if not create or not extracted:
            return  # Simple build, or nothing to add, do nothing
        # Add the iterable of groups using bulk addition
        self.tags.add(*extracted)


class ProductVariantFactory(DjangoModelFactory):
    class Meta:
        model = ProductVariant
    product = SubFactory(ProductFactory)
    variant_name = FuzzyText()
    variant_value = FuzzyText()
    sku = FuzzyText(length=8)
    price = FuzzyDecimal(999999.99)


class CustomerRatingFactory(DjangoModelFactory):
    class Meta:
        model = CustomerRating
    product = SubFactory(ProductFactory)
    rating = FuzzyInteger(1, 5)


class PriceHistoryFactory(DjangoModelFactory):
    class Meta:
        model = PriceHistory

    product_variant = SubFactory(ProductVariantFactory)
    price = FuzzyDecimal(999999.99)
