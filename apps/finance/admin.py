from django.contrib import admin

# Register your models here.

from .models import Category, Transaction, Budget

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_default', 'created_at')
    list_filter = ('is_default', 'user')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'type', 'user', 'date')
    list_filter = ('type', 'date')

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('category', 'limit_amount', 'month', 'year', 'user')