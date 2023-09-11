from collections import namedtuple
from unittest.mock import patch

from django.test import TestCase
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.test import APITestCase

from store.api.permissions import TokenHasAdminScope, UserReadsAdminWrites
from store.api.serializers import ProductVariantSerializer, ProductDetailSerializer, SimpleProductSerializer
from store.api.viewsets import ProductViewSet
from store.factories import ProductVariantFactory, PriceHistoryFactory, CustomerRatingFactory, ProductFactory
from store.models import Tag


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
