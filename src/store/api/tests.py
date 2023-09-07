from rest_framework.test import APITestCase

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
