from itertools import cycle
from unittest.mock import patch

from django.test import TestCase

from store.admin import ReadOnlyAdminMixin
from store.factories import CustomerRatingFactory, ProductVariantFactory, ProductFactory, PriceHistoryFactory, \
    TagFactory, SupplierFactory
from store.models import Tag, Product
from store.signals import customer_rating_post_save, product_variant_post_save
from store.tasks import update_rating


class TagTestCase(TestCase):
    def test_str_should_return_name(self):
        name = 'xyz'
        tag = Tag(name=name)
        self.assertEqual(str(tag), name)


class ReadOnlyAdminMixinTestCase(TestCase):
    def setUp(self):
        self.request = None
        self.instance = ReadOnlyAdminMixin()

    def test_has_no_add_permission(self):
        self.assertFalse(self.instance.has_add_permission(self.request))

    def test_has_no_change_permission(self):
        self.assertFalse(self.instance.has_change_permission(self.request))

    def test_has_no_delete_permission(self):
        self.assertFalse(self.instance.has_delete_permission(self.request))


class SignalsTestCase(TestCase):

    @patch('store.tasks.update_rating.delay')
    def test_customer_rating_post_save_calls_update_rating(self, mock):
        customer_rating = CustomerRatingFactory()
        mock.reset_mock()
        customer_rating_post_save(None, customer_rating)
        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)

    def test_product_variant_post_save_creates_history(self):
        product_variant = ProductVariantFactory()
        previous_history_count = product_variant.price_history.count()
        product_variant_post_save(None, product_variant)
        history_count = product_variant.price_history.count()
        self.assertEqual(history_count - previous_history_count, 1)


class TasksTestCase(TestCase):
    def test_update_rating_calculates_the_average_of_ratings(self):
        product = ProductFactory()
        ratings_to_create = 10
        customer_ratings = CustomerRatingFactory.create_batch(ratings_to_create, product=product)
        rating_sum = 0
        for customer_rating in customer_ratings:
            rating_sum += customer_rating.rating
        calculated_rating_average = rating_sum / len(customer_ratings)
        update_rating(product.id)
        self.assertAlmostEqual(calculated_rating_average, Product.objects.get(id=product.id).rating)


class ModelsTestCase(TestCase):
    def test_tag_str_returns_name(self):
        tag = TagFactory()
        self.assertEqual(str(tag), tag.name)

    def test_supplier_str_returns_name(self):
        supplier = SupplierFactory()
        self.assertEqual(str(supplier), supplier.name)

    def test_product_related_returns_has_same_tags(self):
        tags_cycle = cycle(TagFactory.create_batch(10))
        products = ProductFactory.create_batch(100)
        for product in products:
            for _ in range(3):
                product.tags.add(next(tags_cycle))
        original_product_tags = set(products[0].tags.all())
        for related_product in products[0].related_products:
            related_products_tags = set(related_product.tags.all())
            self.assertGreaterEqual(len(related_products_tags.intersection(original_product_tags)), 1)

    def test_product_related_returns_only_10_products(self):
        tag = TagFactory()
        products = ProductFactory.create_batch(100, tags=[tag])
        self.assertEqual(products[0].related_products.count(), 10)

    def test_product_related_returns_only_distinct_products(self):
        tag = TagFactory()
        products = ProductFactory.create_batch(100, tags=[tag])
        related_products_id = set()
        for related_product in products[0].related_products:
            related_products_id.add(related_product.id)
        self.assertEqual(len(related_products_id), products[0].related_products.count())

    def test_product_related_returns_not_include_self(self):
        tag = TagFactory()
        products = ProductFactory.create_batch(100, tags=[tag])
        related_products_id = set()
        for related_product in products[0].related_products:
            related_products_id.add(related_product.id)
        self.assertNotIn(products[0].id, related_products_id)

    def test_product_str_returns_name(self):
        product = ProductFactory()
        self.assertEqual(str(product), product.name)

    def test_product_variant_str(self):
        product_variant = ProductVariantFactory()
        expected = f'{product_variant.product.name} - {product_variant.variant_name}:{product_variant.variant_value}'
        self.assertEqual(str(product_variant), expected)

    def test_customer_rating_str(self):
        customer_rating = CustomerRatingFactory()
        expected = f'{customer_rating.product.name} rating of {customer_rating.rating}'
        self.assertEqual(str(customer_rating), expected)

    def test_price_history_str(self):
        price_history = PriceHistoryFactory()
        expected = f'{price_history.product_variant} price update at {price_history.updated_at}'
        self.assertEqual(str(price_history), expected)
