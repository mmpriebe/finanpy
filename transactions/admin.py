from django.contrib import admin

from transactions.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'user', 'account', 'category', 'amount', 'transaction_type', 'date')
    list_filter = ('transaction_type', 'date', 'category')
    search_fields = ('description',)
    readonly_fields = ('created_at', 'updated_at')
