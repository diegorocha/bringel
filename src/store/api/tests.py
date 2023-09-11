from collections import namedtuple
from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase
from factory.fuzzy import FuzzyText, FuzzyInteger, FuzzyDecimal
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.models import Application
from rest_framework.test import APITestCase, APIClient

from store.api.permissions import TokenHasAdminScope, UserReadsAdminWrites
from store.api.serializers import ProductVariantSerializer, ProductDetailSerializer, SimpleProductSerializer
from store.api.viewsets import ProductViewSet
from store.factories import ProductVariantFactory, PriceHistoryFactory, CustomerRatingFactory, ProductFactory, \
    TagFactory
from store.models import Tag, PriceHistory


class TagAPITestCase(APITestCase):
    def test_name_should_be_unique(self):
        tag = {"name": "ofertas"}
        another_tag = {"name": "ofertas", "description": "Promoções"}

        response = self.client.post('/api/tags/', tag, format='json')
        self.assertEqual(response.status_code, 201)

        response = self.client.post('/api/tags/', another_tag, format='json')
        self.assertEqual(response.status_code, 400)

        self.assertEqual(Tag.objects.count(), 1)


class TokenHasAdminScopeTestCase(TestCase):
    def test_get_scopes_was_admin_only(self):
        self.assertEqual(TokenHasAdminScope().get_scopes(None, None), ['admin'])


class UserReadsAdminWritesTestCase(TestCase):
    def setUp(self):
        self.request = namedtuple('Request', ['method', 'successful_authenticator', 'auth'])

    def test_is_oauth2_authenticated_false_if_not_successful_authenticator(self):
        method = None
        authenticator = None
        auth = None
        request = self.request(method=method, successful_authenticator=authenticator, auth=auth)
        self.assertFalse(UserReadsAdminWrites().is_oauth2_authenticated(request))

    def test_is_oauth2_authenticated_false_if_not_OAuth2Authentication(self):
        method = None
        authenticator = object()
        auth = None
        request = self.request(method=method, successful_authenticator=authenticator, auth=auth)
        self.assertFalse(UserReadsAdminWrites().is_oauth2_authenticated(request))

    def test_is_oauth2_authenticated_true_if_OAuth2Authentication(self):
        method = None
        authenticator = OAuth2Authentication()
        auth = None
        request = self.request(method=method, successful_authenticator=authenticator, auth=auth)
        self.assertTrue(UserReadsAdminWrites().is_oauth2_authenticated(request))

    @patch('store.api.permissions.TokenHasAdminScope.has_permission')
    def test_has_permission_false_if_is_post_patch_put_delete(self, mock):
        methods = ['POST', 'PATCH', 'PUT', 'DELETE']
        authenticator = OAuth2Authentication()
        auth = None
        mock.return_value = False
        for method in methods:
            request = self.request(method=method, successful_authenticator=authenticator, auth=auth)
            self.assertFalse(UserReadsAdminWrites().has_permission(request, None))

    @patch('store.api.permissions.TokenHasAdminScope.has_permission')
    def test_has_permission_true_if_is_get_head_options(self, mock):
        methods = ['GET', 'HEAD', 'OPTIONS']
        authenticator = OAuth2Authentication()
        auth = None
        mock.return_value = False
        for method in methods:
            request = self.request(method=method, successful_authenticator=authenticator, auth=auth)
            self.assertTrue(UserReadsAdminWrites().has_permission(request, None))

    @patch('store.api.permissions.TokenHasAdminScope.has_permission')
    def test_has_permission_true_if_was_admin(self, mock):
        methods = ['GET', 'HEAD', 'OPTIONS', 'POST', 'PATCH', 'PUT', 'DELETE']
        authenticator = OAuth2Authentication()
        auth = None
        mock.return_value = True
        for method in methods:
            request = self.request(method=method, successful_authenticator=authenticator, auth=auth)
            self.assertTrue(UserReadsAdminWrites().has_permission(request, None))


class ProductVariantSerializerTestCase(TestCase):
    def test_get_price_history_returns_up_to_10_prices(self):
        product_variant = ProductVariantFactory()
        PriceHistoryFactory.create_batch(20, product_variant=product_variant)
        data = ProductVariantSerializer().get_price_history(product_variant)
        self.assertLessEqual(len(data), 10)


class ProductDetailSerializerTestCase(TestCase):
    def test_get_ratings_returns_up_to_10_prices(self):
        product = ProductFactory()
        CustomerRatingFactory.create_batch(20, product=product)
        data = ProductDetailSerializer().get_ratings(product)
        self.assertLessEqual(len(data), 10)

    def test_get_related_products_uses_SimpleProductSerializer(self):
        product = ProductFactory()
        data = ProductDetailSerializer().get_related_products(product)
        self.assertIsInstance(data.serializer.child, SimpleProductSerializer)


class ProductViewSetTestCase(TestCase):
    def test_detailed_uses_ProductDetailSerializer(self):
        product = ProductFactory()
        Request = namedtuple('Request', ['query_params'])
        request = Request(query_params={})
        viewset = ProductViewSet()
        viewset.request = request
        viewset.kwargs = {'pk': product.id}
        response = viewset.detailed(request, pk=product.id)
        self.assertIsInstance(response.data.serializer, ProductDetailSerializer)


class OAuth2AuthMixin:
    def get_oauth_token(self, admin=False):
        client = getattr(self, 'client', APIClient())
        client_id = FuzzyText().fuzz()
        client_secret = FuzzyText().fuzz()
        app_name = FuzzyText().fuzz()
        Application.objects.create(
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
            client_id=client_id,
            client_secret=client_secret,
            name=app_name,
        )
        payload = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
        }
        if admin:
            payload['scope'] = 'admin'
        response = client.post('/oauth2/token/', data=payload)
        return response.json()['access_token']

    def get_oauth_headers(self, admin=False):
        token = self.get_oauth_token(admin)
        return {
            'Authorization': f'Bearer {token}'
        }


class ProductDetailTestCase(OAuth2AuthMixin, APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.oauth_headers = self.get_oauth_headers()

    def test_product_detailed_has_related_products_and_ratings(self):
        tag = TagFactory()
        products = ProductFactory.create_batch(100, tags=[tag])
        response = self.client.get(f'/api/products/{products[0].id}/detailed/', headers=self.oauth_headers)
        self.assertIn('related_products', response.data)
        self.assertIn('ratings', response.data)


class CustomerRatingsTestCase(OAuth2AuthMixin, APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.oauth_headers = self.get_oauth_headers()

    def test_customer_rating_must_be_between_1_and_5(self):
        product = ProductFactory()
        self.assertIsNone(product.rating)
        boundaries = [-1, 0, 6, 7]
        for rating in boundaries:
            payload = {
                'product': product.id,
                'rating': rating,
                'description': FuzzyText().fuzz(),
            }
            response = self.client.post('/api/products/rating/', headers=self.oauth_headers, data=payload)
            self.assertEqual(response.status_code, 400)
            self.assertIn('rating', response.json())
        product.refresh_from_db()
        self.assertIsNone(product.rating)
        valids = range(1, 6)
        for rating in valids:
            payload = {
                'product': product.id,
                'rating': rating,
                'description': FuzzyText().fuzz(),
            }
            response = self.client.post('/api/products/rating/', headers=self.oauth_headers, data=payload)
            self.assertEqual(response.status_code, 201)
        product.refresh_from_db()
        self.assertAlmostEqual(product.rating, 3.0)

    def test_new_customer_rating_updates_product_rating(self):
        product = ProductFactory()
        self.assertIsNone(product.rating)
        new_rating = FuzzyInteger(1, 5).fuzz()
        payload = {
            'product': product.id,
            'rating': new_rating,
            'description': FuzzyText().fuzz(),
        }
        response = self.client.post('/api/products/rating/', headers=self.oauth_headers, data=payload)
        self.assertEqual(response.status_code, 201)
        product.refresh_from_db()
        self.assertAlmostEqual(product.rating, new_rating)

    def test_multiple_customer_rating_updates_product_rating(self):
        product = ProductFactory()
        self.assertIsNone(product.rating)
        ratings = []
        for _ in range(15):
            ratings.append(FuzzyInteger(1, 5).fuzz())
        new_rating = sum(ratings) / len(ratings)
        for rating in ratings:
            payload = {
                'product': product.id,
                'rating': rating,
                'description': FuzzyText().fuzz(),
            }
            response = self.client.post('/api/products/rating/', headers=self.oauth_headers, data=payload)
            self.assertEqual(response.status_code, 201)

        product.refresh_from_db()
        self.assertAlmostEqual(product.rating, new_rating)


class PriceHistoryTestCase(OAuth2AuthMixin, APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.oauth_headers = self.get_oauth_headers()

    def test_product_variant_price_changes_create_price_history(self):
        product_variant = ProductVariantFactory()
        self.assertEqual(PriceHistory.objects.filter(product_variant=product_variant.id).count(), 1)
        new_price = FuzzyDecimal(999999.99).fuzz()
        payload = {
            'price': new_price,
        }
        response = self.client.patch(
            f'/api/products/variants/{product_variant.id}/',
            headers=self.get_oauth_headers(admin=True),
            data=payload,
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f'/api/products/variants/{product_variant.id}/', headers=self.oauth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['price_history']), 2)

    def test_product_variant_price_changes_retuns_up_to_10_price_histories(self):
        product_variant = ProductVariantFactory()
        for _ in range(15):
            payload = {
                'price': FuzzyDecimal(999999.99).fuzz(),
            }
            response = self.client.patch(
                f'/api/products/variants/{product_variant.id}/',
                headers=self.get_oauth_headers(admin=True),
                data=payload,
            )
            self.assertEqual(response.status_code, 200)
        response = self.client.get(f'/api/products/variants/{product_variant.id}/', headers=self.oauth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['price_history']), 10)

    def test_price_history_desc_order(self):
        product_variant = ProductVariantFactory()
        price_changes = [product_variant.price]
        for _ in range(5):
            new_price = FuzzyDecimal(999999.99).fuzz()
            price_changes.append(new_price)
            payload = {
                'price': new_price,
            }
            response = self.client.patch(
                f'/api/products/variants/{product_variant.id}/',
                headers=self.get_oauth_headers(admin=True),
                data=payload,
            )
            self.assertEqual(response.status_code, 200)

        response = self.client.get(f'/api/products/variants/{product_variant.id}/', headers=self.oauth_headers)
        self.assertEqual(response.status_code, 200)
        price_history = []
        for history in response.data['price_history']:
            price_history.append(Decimal(history['price']))
        self.assertEqual(price_history, list(reversed(price_changes)))
