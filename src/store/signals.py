import logging

from store.tasks import update_rating

logger = logging.getLogger(__name__)


def customer_rating_post_save(sender, instance, **__):
    logger.info("Received customer_rating_post_save", extra={"product_id": instance.product.id})
    update_rating.delay(instance.product.id)
    logger.info('Created task update_rating', extra={'product_id': instance.product.id})
    return
