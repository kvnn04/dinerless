from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.users.models import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Categories"
        # para que no haya dos "Comida" para el mismo usuario
        unique_together = ['user', 'name'] 
        indexes = [
            models.Index(fields=['user'], name='category_user_idx'),
        ]

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class Transaction(BaseModel):
    TRANSACTION_TYPES = [
        ('INCOME', 'Ingreso'),
        ('EXPENSE', 'Gasto'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=255, blank=True)
    # Cambiado para que el usuario pueda elegir la fecha si quiere
    date = models.DateTimeField(default=timezone.now) 

    class Meta:
        ordering = ['-date'] # Las últimas transacciones primero
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
    month = models.PositiveSmallIntegerField() 
    year = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ['user', 'category', 'month', 'year']
        indexes = [
            models.Index(fields=['user', 'month', 'year'], name='budget_lookup_idx'),
        ]

    def __str__(self):
        return f"Presupuesto {self.month}/{self.year} - {self.category.name}"