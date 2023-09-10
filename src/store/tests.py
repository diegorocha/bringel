from unittest.mock import patch

from django.test import TestCase

from store.admin import ReadOnlyAdminMixin
from store.factories import CustomerRatingFactory, ProductVariantFactory, ProductFactory
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
