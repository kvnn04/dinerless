from rest_framework import serializers
from apps.finance.models import Category, Transaction, Budget
from rest_framework.validators import UniqueTogetherValidator
from django.utils import timezone

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'is_default', 'created_at']
        read_only_fields = ['id', 'created_at']

        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=['user', 'name'],
                message="Ya tienes una categoría con este nombre."
            )
        ]
        
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("El nombre es demasiado corto.")
        return value.strip()

    def validate_icon(self, value):
        if len(value) > 50:
            raise serializers.ValidationError(f"Icono demasiado largo ({len(value)}/50).")
        if not value.strip():
            raise serializers.ValidationError("El icono no puede estar vacío.")
        return value

class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Transaction
        fields = ['id', 'category', 'category_name', 'amount', 'description', 'type', 'date', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser mayor a cero.")
        return value

    def validate_date(self, value):
        if value > timezone.now().date() + timezone.timedelta(days=365):
            raise serializers.ValidationError("La fecha es demasiado lejana en el futuro.")
        return value

class BudgetSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Budget
        fields = ['id', 'category', 'category_name', 'limit_amount', 'month', 'year']
        read_only_fields = ['id']

        validators = [
            UniqueTogetherValidator(
                queryset=Budget.objects.all(),
                fields=['user', 'category', 'month', 'year'],
                message="Ya existe un presupuesto para este periodo."
            )
        ]

    def validate_limit_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("El límite debe ser mayor a cero.")
        return value

    def validate_month(self, value):
        if value < 1 or value > 12:
            raise serializers.ValidationError("Mes inválido.")
        return value

    def validate_year(self, value):
        current_year = timezone.now().year
        if value < current_year - 1 or value > current_year + 5:
            raise serializers.ValidationError(f"Año fuera de rango ({current_year-1} a {current_year+5}).")
        return value