from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from apps.users.models import BaseModel # <--- Importas tu base

class Category(BaseModel):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=['user'], name='category_user_idx'),
        ]

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class Transaction(BaseModel):
    TRANSACTION_TYPES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(auto_now_add=True) # <--- Agrega esto

    class Meta:
        indexes = [
            models.Index(fields=['user', 'date'], name='transaction_user_date_idx'),
            models.Index(fields=['type'], name='transaction_type_idx'),
        ]

    def __str__(self):
        return f"{self.type}: {self.amount} - {self.user.username}"

class Budget(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    limit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.PositiveSmallIntegerField() # 1-12
    year = models.PositiveSmallIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['user', 'month', 'year'], name='budget_lookup_idx'),
        ]
        # Evita que un usuario tenga dos presupuestos para la misma categoría en el mismo mes/año
        unique_together = ['user', 'category', 'month', 'year']

    def __str__(self):
        return f"Budget {self.month}/{self.year} - {self.category.name}"