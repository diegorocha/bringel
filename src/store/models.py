from django.db import models


class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']
    name = models.CharField('Name', max_length=50, blank=False, null=False, unique=True)
    description = models.CharField('Description', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        ordering = ['name']
    name = models.CharField('Name', max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='products')
    name = models.CharField('Name', max_length=50, blank=False, null=False)
    description = models.TextField('Description', blank=False, null=False)
    tags = models.ManyToManyField(Tag, related_name='products')
    rating = models.FloatField('Rating', null=True, blank=True)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    class Meta:
        verbose_name = 'Product Variant'
        verbose_name_plural = 'Product Variants'
        ordering = ['product', 'variant_name', 'variant_value']
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='variants')
    variant_name = models.CharField('Variant Name', max_length=20, blank=False, null=False)
    variant_value = models.CharField('Variant Value', max_length=50, blank=False, null=False)
    sku = models.CharField('SKU', max_length=8, blank=False, null=False)
    in_stock = models.BooleanField('In Stock',  blank=True, default=False)
    price = models.DecimalField('Price', max_digits=8, decimal_places=2, blank=False, null=False)

    def __str__(self):
        return f'{self.product.name} - {self.variant_name}:{self.variant_value}'


class CustomerRating(models.Model):
    class Meta:
        verbose_name = 'Customer Rating'
        verbose_name_plural = 'Customer Ratings'
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                check=models.Q(rating__gte=1) & models.Q(rating__lte=5),
                name="Rating must be between 1 and 5",
            )
        ]
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='ratings')
    rating = models.IntegerField('Rating', blank=False, null=False)
    description = models.TextField('Description', max_length=100, blank=False, null=False)
    created_at = models.DateTimeField('Created At', auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} rating of {self.rating}'


class PriceHistory(models.Model):
    class Meta:
        verbose_name = 'Price History'
        verbose_name_plural = 'Price History'
        ordering = ['-updated_at']
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, related_name='price_history')
    price = models.DecimalField('Price', max_digits=8, decimal_places=2, blank=False, null=False)
    updated_at = models.DateTimeField('Updated At', auto_now_add=True)

    def __str__(self):
        return f'{self.product_variant} price update at {self.updated_at}'
