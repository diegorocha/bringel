import logging

from django.apps import apps

from store.tasks import update_rating

logger = logging.getLogger(__name__)


def customer_rating_post_save(sender, instance, **__):
    logger.info("Received customer_rating_post_save", extra={"product_id": instance.product.id})
    update_rating.delay(instance.product.id)
    logger.info('Created task update_rating', extra={'product_id': instance.product.id})


def product_variant_post_save(sender, instance, **__):
    logger.info("Received product_variant_post_save", extra={"product_variant_id": instance.id})
    logger.info('Updating price history', extra={'product_variant_id': instance.id})
    model_price_history = apps.get_model(app_label='store', model_name='PriceHistory')
    model_price_history.objects.create(product_variant_id=instance.id, price=instance.price)
