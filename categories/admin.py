from django.contrib import admin

from categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'transaction_type', 'is_active')
    list_filter = ('transaction_type', 'is_active')
    search_fields = ('name', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
