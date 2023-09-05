import logging

from celery import shared_task
from django.apps import apps
from django.db.models import Avg


logger = logging.getLogger(__name__)


@shared_task(serializer='json')
def update_rating(product_id):
    logger.info(f'Updating rating of product {product_id}', extra={'product_id': product_id})
    product_model = apps.get_model(app_label='store', model_name='Product')
    product = product_model.objects.get(id=product_id)
    aggregate = product.ratings.aggregate(rating=Avg('rating'))
    rating = aggregate['rating']
    logger.info(f'New rating of product {product_id}: {rating}', extra={'product_id': product_id, 'rating': rating})
    product.rating = rating
    product.save()
