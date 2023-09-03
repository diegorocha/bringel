from django.contrib import admin

from store.models import Tag, Supplier, Product, ProductVariant, CustomerRating


class ReadOnlyAdminMixin:
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['rating']


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomerRating)
class CustomerRatingAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ['product', 'rating', 'created_at']
