from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'brand',
        'price',
        'price',
        'available',
        'created_at',
        'update_at'
    )
    list_filter = ('available', 'created_at', 'update_at')
    ordering = ('title',)

    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('title',)
        }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    ordering = ('name',)

    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('name',)
        }
