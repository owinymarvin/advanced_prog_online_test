from django.contrib import admin
from .models import Product, DiscountedProduct, CalculatedProduct
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    search_fields = ('name',)
    list_filter = ('price',)

    def has_add_permission(self, request):
        """Restrict add permission for non-admin users."""
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        """Restrict change permission to a certain group."""
        return request.user.groups.filter(name='Product Managers').exists()


class DiscountedProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount_percentage')
    list_filter = ('discount_percentage',)


class CalculatedProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'additional_fee')


admin.site.register(Product, ProductAdmin)
admin.site.register(DiscountedProduct, DiscountedProductAdmin)
admin.site.register(CalculatedProduct, CalculatedProductAdmin)
